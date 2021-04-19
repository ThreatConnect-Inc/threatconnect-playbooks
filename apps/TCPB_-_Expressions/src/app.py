# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

import json
import re
import sys
import traceback

from lark_expr import Expression
from argcheck import tc_argcheck
from trap_exception import trap

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp

identifierRE = re.compile(r'^[A-Za-z_]\w*$')

# pylint: disable=assignment-from-none,assignment-from-no-return


class IterTracker(object):
    """Track iterables"""

    def __init__(self):
        self.names = []
        self.values = {}
        self.index = 0
        self.len = None

    def add(self, name, value):
        """add a value to the tracker"""

        ln = len(value)
        if self.len is not None and ln != self.len:
            raise ValueError(f'Tracker for {name} has different length')
        self.names.append(name)
        self.values[name] = value
        self.len = ln

    def next(self, wrap=True):
        """ Get a dictionary of the next values of this tracker or None if complete """

        self.index += 1

        if self.index >= self.len:
            if wrap:
                self.index = 0
            else:
                return None

        result = {}
        for name in self.names:
            result[name] = self.values[name][self.index]

        return result

    def current(self):
        """Get the current values"""

        if self.index >= self.len:
            return None

        index = self.index
        if index < 0:
            index = 0

        result = {}
        for name in self.names:
            result[name] = self.values[name][index]

        return result


class App(PlaybookApp):
    """Playbook App"""

    def __init__(self, tcex_):
        """init"""
        super().__init__(tcex_)
        self.engine = Expression(tcex_)

        self.expression = ''
        self.output = []
        self.outlist = []
        self.errors = []
        self.loop = None
        self.outloop = {}

    def handle_exception(self, exception, force_exit=False):
        """handle exception"""

        return_none_on_failure = tc_argcheck(
            self.tcex.args, 'return_none_on_failure', tcex=self.tcex
        )

        self.errors.append(str(exception))
        self.tcex.log.error(str(exception))

        tb = sys.exc_info()[2]
        while tb and tb.tb_next:
            tb = tb.tb_next

        if tb:
            name = tb.tb_frame.f_code.co_name
            args = []
            for arg in tb.tb_frame.f_code.co_varnames:
                value = repr(tb.tb_frame.f_locals.get(arg))
                if len(value) > 12:
                    value = value[:12] + '...'
                    if value.startswith('"'):
                        value += '"'
                    elif value.startswith("'"):
                        value += "'"
                    elif value.startswith('{'):
                        value += '}'
                args.append(f'{arg}={value}')
            args = ', '.join(args)
            self.tcex.log.debug(f'Error during {name}({args})')

        error = traceback.format_exc()
        self.tcex.log.debug(error)
        if force_exit or not return_none_on_failure:
            self.tcex.playbook.exit(1, str(exception))

    def setup_loops(self, varname):
        """ Read the Key Value Array in, and setup iter_control """

        loopvars = tc_argcheck(self.tcex.args, varname, required=True, tcex=self.tcex)
        loopvars = self.tcex.playbook.read(loopvars, array=True, embedded=False)
        self.tcex.log.debug(f'Loopvars are {loopvars}')

        sizes = []
        for var in loopvars:
            key = var['key']
            if not identifierRE.match(key):
                self.handle_exception(
                    f'Invalid loop variable {key}.  Variables must start with a letter '
                    'and contain only letters, numbers, and underscore.',
                    force_exit=True,
                )
            value = var['value']
            self.tcex.log.debug(f'Retrieving values for {key} from {value!r}')
            if isinstance(value, str):
                try:
                    value = self.engine.eval(value)
                except Exception as e:
                    value = self.handle_exception(
                        f'Unable to get values for loop variable {key}: {e}'
                    )

            if not isinstance(value, (list, tuple)):
                value = (value,)
                self.tcex.log.debug(f'Loop variable {key} is {value!r}')
            sizes.append((len(value), key, value))

        sizes.sort()  # trackers from smallest to largest

        iter_control = []
        lastsize = None
        tracker = None
        for s, name, value in sizes:
            if s != lastsize:
                if tracker:
                    iter_control.append(tracker)
                lastsize = s
                tracker = IterTracker()
            tracker.add(name, value)

        if tracker:
            iter_control.append(tracker)

        return iter_control

    def setup_outputs(self, varname, required=True, output_type='String'):
        """ Setup output varables from expressions """
        out_list = tc_argcheck(self.tcex.args, varname, required=required, tcex=self.tcex)
        out_list = self.tcex.playbook.read(out_list, array=True, embedded=False)

        if not out_list:
            return

        for out in out_list:
            name = out['key']
            value = out['value']
            self.tcex.log.debug(f'Setting {name} from {value}')
            try:
                if value:
                    value = self.engine.eval(value)
            except Exception as e:
                value = self.handle_exception(
                    f'Error evaluating {name}: {e}.  For string literals, enclose them in quotes.'
                )

            self.engine.set(name, value)  # allow outputs to see prior outputs

            if isinstance(value, (list, tuple, dict)) and output_type in ('String', 'Binary'):
                value = json.dumps(value, sort_keys=True, ensure_ascii=False)

            if output_type.endswith('Array') and not isinstance(value, (list, tuple)):
                self.tcex.log.debug('... promoting to array')
                value = [value]

            self.tcex.log.debug(f'... {name} = {value!r}')

            self.outlist.append((name, value, output_type))

    def setup_vars(self, varname):
        """Setup initial variables"""
        var_list = tc_argcheck(self.tcex.args, varname, tcex=self.tcex)

        if var_list:
            var_list = self.tcex.playbook.read(var_list, array=True, embedded=False)

        if not var_list:
            var_list = []

        for var in var_list:
            name = var['key']
            if not identifierRE.match(name):
                self.handle_exception(
                    f'Invalid variable {name}.  Variables must start with a letter and '
                    'contain only letters, numbers, and underscore.',
                    force_exit=True,
                )
            value = var['value']
            self.tcex.log.debug(f'Setting {name} from {value}')
            try:
                if value:
                    value = self.engine.eval(value)
            except Exception as e:
                value = self.handle_exception(
                    f'Error evaluating {name}: {e}.  For string literals, enclose them in quotes.'
                )

            self.tcex.log.debug(f'... {name} = {value!r}')
            self.engine.set(name, value)

    def loop_over_iter(self, iter_control, exprs=None):
        """Loop over iter_control variables, returns a dict of outputs"""

        if exprs is None:
            exprs = {}

        if isinstance(exprs, str):
            exprs = {'output': exprs}

        for key in exprs:
            self.tcex.log.debug(f'Loop expression "{key}": "{exprs[key]}"')

        outdict = {}

        looping = True
        loopcount = 0
        get_next = False

        # 1.0.6 -- set individual loop values with leading underscore to None
        for key in exprs:
            self.engine.set('_' + key, None)

        while looping:
            # t  Trackers are ordered from shortest to longest
            # inner trackers need to wrap around until the longest tracker
            # completes
            this_iter = iter_control.copy()
            if loopcount:
                get_next = True
            self.tcex.log.trace('***Calculating next iteration***')
            while this_iter:
                tracker = this_iter.pop(0)

                if get_next:
                    vars_ = tracker.next(wrap=False)
                else:
                    vars_ = tracker.current()

                get_next = False

                if vars_ is None:
                    get_next = True
                    if this_iter:
                        self.tcex.log.trace(f'Wrapping {tracker.names}')
                        vars_ = tracker.next(wrap=True)
                    else:
                        looping = False

                if vars_:
                    for key, value in vars_.items():
                        self.tcex.log.trace(f'Setting value {key} to {value!r}')
                        self.engine.set(key, value)

            if looping or loopcount == 0:
                for expr_key, expr_value in exprs.items():
                    self.tcex.log.trace(f'Evaluating... {expr_key} = {expr_value}')
                    try:
                        result = self.engine.eval(expr_value)
                    except Exception as e:
                        result = self.handle_exception(f'Evaluation of "{expr_key}" failed: {e}')
                    self.tcex.log.trace(f'... = {result!r}')

                    # 1.0.6 -- add individual loop result with leading underscore
                    self.engine.set('_' + expr_key, result)

                    out = outdict.get(expr_key, [])

                    # 1.0.6 - Don't flatten tuples, just lists
                    if isinstance(result, list):
                        out.extend(result)
                    else:
                        out.append(result)
                    outdict[expr_key] = out

            loopcount += 1

        return outdict

    @trap()
    def Evaluate(self):
        """Evaluate an expression"""

        expr = tc_argcheck(self.tcex.args, 'expression', required=True, tcex=self.tcex)
        self.expression = self.tcex.playbook.read(expr, embedded=True)
        expr = self.tcex.playbook.read(expr, embedded=False)
        self.tcex.log.info(f'Evaluating expression {expr!r}')

        try:
            result = self.engine.eval(expr)
        except Exception as e:
            result = self.handle_exception(f'Evaluation of "{expr}" failed: {e}')

        if isinstance(result, list):
            self.output.extend(result)
        else:
            self.output.append(result)

    @trap()
    def evaluate_in_loop(self):
        """Evaluate an expression in a loop"""

        iter_control = self.setup_loops('loop_variables')

        expr = tc_argcheck(
            self.tcex.args, 'loop_expression', required=True, tcex=self.tcex, label='Expression'
        )

        expr = self.tcex.playbook.read(expr, embedded=False)

        self.expression = self.tcex.playbook.read(expr, embedded=True)

        self.tcex.log.debug(f'Expression is {expr}')

        outdict = self.loop_over_iter(iter_control, expr)

        self.output = outdict.get('output')

    @trap()
    def evaluate_many(self):
        """Evaluate many expressions"""

        self.setup_vars('variables')
        self.setup_outputs('outputs')
        self.setup_outputs('binary_outputs', required=False, output_type='Binary')
        self.setup_outputs('binary_array_outputs', required=False, output_type='BinaryArray')
        self.setup_outputs('kv_outputs', required=False, output_type='KeyValue')
        self.setup_outputs('kv_array_outputs', required=False, output_type='KeyValueArray')
        self.setup_outputs('tce_outputs', required=False, output_type='TCEntity')
        self.setup_outputs('tce_array_outputs', required=False, output_type='TCEntityArray')
        self.setup_outputs('tcee_outputs', required=False, output_type='TCEnhancedEntity')
        self.setup_outputs(
            'tcee_array_outputs', required=False, output_type='TCEnhancedEntityArray'
        )

    @trap()
    def evaluate_many_with_loop(self):
        """Evaluate many expressions with loop variables"""

        self.setup_vars('variables')
        iter_control = self.setup_loops('loop_variables')

        exprs = tc_argcheck(self.tcex.args, 'loop_expressions', required=True, tcex=self.tcex)
        if exprs:
            exprs = self.tcex.playbook.read(exprs, embedded=False)

        loop_exprs = {}
        for expr in exprs:
            key = expr['key']
            value = expr['value']
            loop_exprs[key] = value

        self.outloop = self.loop_over_iter(iter_control, loop_exprs)

        for key, value in self.outloop.items():
            self.engine.set(key, value)

        self.setup_outputs('additional_outputs', required=False)
        self.setup_outputs('binary_outputs', required=False, output_type='Binary')
        self.setup_outputs('binary_array_outputs', required=False, output_type='BinaryArray')
        self.setup_outputs('kv_outputs', required=False, output_type='KeyValue')
        self.setup_outputs('kv_array_outputs', required=False, output_type='KeyValueArray')
        self.setup_outputs('tce_outputs', required=False, output_type='TCEntity')
        self.setup_outputs('tce_array_outputs', required=False, output_type='TCEntityArray')
        self.setup_outputs('tcee_outputs', required=False, output_type='TCEnhancedEntity')
        self.setup_outputs(
            'tcee_array_outputs', required=False, output_type='TCEnhancedEntityArray'
        )

    def write_one(self, name, value, output_type):
        """Write one output"""

        # JSON-ify any array outputs that are compound for the text outputs
        if output_type in ('StringArray', 'BinaryArray'):
            result = []
            for entry in value:
                if isinstance(entry, (list, dict, tuple)):
                    entry = json.dumps(entry, sort_keys=True)
                result.append(entry)
            value = result

        if output_type in ('String', 'Binary') and isinstance(value, (dict, list, tuple)):
            value = json.dumps(value, sort_keys=True)

        self.tcex.log.debug(f'Write: {name}!{output_type}={value!r}')
        try:
            self.tcex.playbook.create_output(name, value, output_type)
        except Exception as e:
            return_none_on_failure = tc_argcheck(
                self.tcex.args, 'return_none_on_failure', tcex=self.tcex
            )
            self.tcex.log.error(f'Error creating output {name}: {e}')
            self.errors.append(f'Error creating output {name}: {e}')
            if not return_none_on_failure:
                self.tcex.playbook.exit(1, f'Unable to create output {name}: {e}')

    def write_output(self):
        """Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.
        """

        self.tcex.playbook.create_output('expression.action', self.tcex.args.tc_action, 'String')
        if self.expression:
            self.tcex.playbook.create_output('expression.expression', self.expression, 'String')
        if self.output:
            self.write_one('expression.result.0', self.output[0], 'String')
            self.write_one('expression.result.array', self.output, 'StringArray')
        if self.outlist:
            for name, value, output_type in self.outlist:
                self.write_one(name, value, output_type)
        if self.outloop:
            for name, value in self.outloop.items():
                self.write_one(name, value, 'StringArray')
        if self.errors:
            self.tcex.playbook.create_output('expression.errors', self.errors, 'StringArray')
