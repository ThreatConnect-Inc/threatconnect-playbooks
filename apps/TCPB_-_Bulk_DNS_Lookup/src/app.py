"""ThreatConnect Playbook App"""

# standard library
import json
import time
import traceback
from threading import Lock, Thread
from urllib.parse import urlparse

# third-party
import dns.exception
import dns.message
import dns.query
import dns.resolver

# first-party
from argcheck import tc_argcheck
from json_util import conform_objects, refold
from playbook_app import PlaybookApp  # Import default Playbook App Class (Required)
from trap_exception import trap

TIMEOUT = 3


class Throttle:
    """Throttle Class"""

    def __init__(self, rate=150):
        """Create a throttle for a specific rate/sec"""

        self.lock = Lock()
        self.rate = rate
        self.ts = None
        self.count = 0

    def __call__(self):
        """Return when the throttle limit is acceptable"""

        with self.lock:
            now = time.time()
            if self.ts is None:
                self.ts = now

            if now - self.ts >= 1.0:
                self.count = 0
                self.ts = now

            self.count += 1

            if self.count <= self.rate:
                return

            time.sleep(self.ts + 1 - now)


class App(PlaybookApp):
    """Playbook App"""

    def __init__(self, _tcex):
        """Initialize class properties."""
        super().__init__(_tcex)

        self.outputs = []
        self.exit_code = 0
        self.exit_message = 'Success.'
        self.questions = []
        self.answers = []
        self.throttle = None
        self.cache = dns.resolver.LRUCache()
        self.nameservers = None
        self.transform_ptr = True

    def add_output(self, name, value, jsonify=False):
        """Add an output to the output list"""

        self.outputs.append((name, value, jsonify))

    @trap()
    def lookup_dns(self) -> None:
        """Run the App main logic.

        This method should contain the core logic of the App.
        """

        questions = tc_argcheck(
            self.tcex.rargs, 'questions', label='Question(s)', required=True, tcex=self.tcex
        )

        if not isinstance(questions, list):
            questions = [questions]

        record_types = tc_argcheck(self.tcex.rargs, 'record_types', required=True, tcex=self.tcex)

        if not isinstance(record_types, list):
            record_types = [record_types]

        record_types = [x for x in record_types if x]

        if not record_types:
            self.fail('At least one resource record type is required.')

        self.tcex.log.debug(f'Questions: {questions!r}, rrtypes {record_types!r}')

        for question in questions:

            if isinstance(question, dict):  # must be tcentity
                entity_type = question.get('type')
                question = question.get('value')

                if entity_type == 'EmailAddress':
                    if '@' not in question:
                        self.tcex.log.warning(f'Invalid EmailAddress {question} -- Skipped')
                        continue
                    question = question.split('@', 1)[1]
                elif entity_type == 'Address':
                    pass
                elif entity_type == 'Host':
                    pass
                elif entity_type.upper() == 'URL':
                    question = urlparse(question).netloc
                else:
                    self.tcex.log.warning(f'Unexpected indicator type {entity_type} -- Skipped')
                    continue

            for rrtype in record_types:
                self.questions.append((question, rrtype))

        self.tcex.log.debug(f'Queuing {len(self.questions)} for resolution')

        self.batch_resolve()

        result = {}
        cnames = {}
        valid_questions = set()
        invalid_questions = set()

        for answer in self.answers:
            question, cname, answers = answer
            qname, rrtype = question

            rrdict = result.get(qname, {})
            result[qname] = rrdict
            alist = rrdict.get(rrtype, [])
            rrdict[rrtype] = alist

            if answers:
                valid_questions.add(qname)

                for a in answers:
                    if a not in alist:
                        alist.append(a)

            if qname not in cnames:
                cnames[qname] = cname

        for answer in self.answers:
            question, cname, answers = answer
            qname, rrtype = question

            if qname not in valid_questions:
                invalid_questions.add(qname)

        self.add_output('dns.result.json', result, jsonify=True)
        self.add_output('dns.valid', sorted(list(valid_questions)))
        self.add_output('dns.invalid', sorted(list(invalid_questions)))

    def fail(self, exit_message):
        """Exit with failure message, but after writing output"""
        self.exit_code = 1
        self.exit_message = exit_message
        self.write_output()

    @property
    def fail_on_no_results(self):
        """Return True if fail_on_no_results is set"""
        return tc_argcheck(
            self.tcex.args, 'fail_on_no_results', types=bool, default=False, tcex=self.tcex
        )

    def handle_exception(self, e):
        """Handle exceptions raised during any trap() decorated method"""

        exit_message = str(e)
        if ' ' not in exit_message:
            exit_message = repr(e)

        self.tcex.log.error(repr(e))
        self.tcex.log.error(traceback.format_exc())

        self.fail(exit_message)

    def setup(self):
        """Perform prep/startup operations."""

        self.nameservers = tc_argcheck(
            self.tcex.rargs, 'dns_servers', label='DNS Servers', required=True, tcex=self.tcex
        )
        rate_limit = tc_argcheck(
            self.tcex.rargs, 'rate_limit', required=True, types=int, default=150, tcex=self.tcex
        )
        self.throttle = Throttle(rate_limit)

        self.transform_ptr = tc_argcheck(
            self.tcex.rargs, 'transform_ptr', default=True, types=bool, tcex=self.tcex
        )

        if isinstance(self.nameservers, str):
            self.nameservers = self.nameservers.split(',')
        if not isinstance(self.nameservers, list):
            self.nameservers = [self.nameservers]

        self.nameservers = [x.strip() for x in self.nameservers]

        self.add_output('dns.action', self.tcex.rargs.tc_action)

    def write_one(self, name, value):
        """Write one output"""
        if isinstance(value, list):
            kind = 'StringArray'
        else:
            kind = 'String'

        if not isinstance(value, (list, dict, int, str, bool, float)) and value is not None:
            value = repr(value)

        self.tcex.playbook.create_output(name, value, kind)

    def write_output(self) -> None:
        """Write the Playbook output variables."""

        for prefix, value, jsonify in self.outputs:
            if callable(value):
                try:
                    value = value()  # deferred action output
                except Exception:
                    self.tcex.log.error(
                        f'Exception raised during output handling for {prefix}, '
                        'writing null output'
                    )
                    value = None
            if jsonify and isinstance(value, (list, dict)):
                value = json.dumps(value)
                self.tcex.log.debug(f'JSONifying output {prefix}')
            if isinstance(value, (list, dict)):
                value = conform_objects(value)
                value = refold(value, prefix=prefix)
                for name, inner_value in value.items():
                    self.write_one(name, inner_value)
            else:
                self.write_one(prefix, value)

        self.tcex.playbook.exit(self.exit_code, self.exit_message)

    def batch_resolve(self, count=4):
        """Fire up count resolver threads, then join on them"""

        threads = []
        for n in range(count):
            threads.append(
                Thread(group=None, target=self.resolver_thread, name=f'Resolver-{n+1}', daemon=True)
            )

        for thread in threads:
            self.tcex.log.debug(f'Starting Resolver {thread.name}')
            thread.start()

        for thread in threads:
            self.tcex.log.debug(f'Joining Resolver {thread.name}')
            thread.join()

    def resolver_thread(self):
        """Resolver Thread to handle DNS lookups"""

        self.tcex.log.debug(f'Resolver starting... {len(self.questions)} questions remaining...')

        try:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.nameservers = self.nameservers
            resolver.timeout = TIMEOUT
            resolver.cache = self.cache
        except Exception as e:
            self.tcex.log.error(f'Failed to create resolver: {e}')
            self.tcex.log.error(traceback.format_exc())

        while self.questions:
            question = self.questions.pop()

            self.throttle()

            self.tcex.log.debug(f'Question: {question}')
            answer = self.resolve(question, resolver)
            cname = None
            if answer:
                result = []
                for rdata in answer:
                    data = rdata.to_text()
                    if data.endswith('.'):
                        data = data[:-1]
                    result.append(data)
                cname = str(answer.canonical_name)
                if cname.endswith('.'):  # it will!
                    cname = cname[:-1]
                answer = result
            self.tcex.log.debug(f'Answer: {question} ({cname})= {answer}')
            self.answers.append((question, cname, answer))

    def resolve(self, question, resolver):
        """Resolve ONE question, in the form of (name, rrtype)"""

        name, rrtype = question

        try:
            if rrtype == 'PTR' and self.transform_ptr:
                answer = resolver.resolve_address(name, lifetime=3, search=False)
            else:
                answer = resolver.resolve(name, rrtype, lifetime=3, search=False)

            return answer

        except dns.exception.Timeout:
            self.tcex.log.debug(f'Timeout resolving {name} {rrtype}')
        except dns.resolver.NXDOMAIN:
            self.tcex.log.debug(f'NXDOMAIN resolving {name} {rrtype}')
        except dns.resolver.YXDOMAIN:
            self.tcex.log.debug(f'YXDOMAIN resolving {name} {rrtype}')
        except dns.resolver.NoAnswer:
            self.tcex.log.debug(f'No answer resolving {name} {rrtype}')
        except dns.resolver.NoNameservers:
            self.tcex.log.debug(f'No nameservers resolving {name} {rrtype}')
        except Exception as e:
            self.tcex.log.error(f'Error resolving question: {e}')
            self.tcex.log.error(traceback.format_exc())

        return None
