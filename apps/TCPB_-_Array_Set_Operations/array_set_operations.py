# -*- coding: utf-8 -*-
""" StringArray Set Playbook App """
import traceback
import sys

from tcex import TcEx

# Python 2 unicode
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

tcex = TcEx()

# App args
tcex.parser.add_argument('--set_a', required=True)
tcex.parser.add_argument('--set_b', required=True)
tcex.parser.add_argument('--set_operation', required=True)
args = tcex.args


def main():
    """Main App Logic"""
    set_a = tcex.playbook.read(args.set_a)
    set_b = tcex.playbook.read(args.set_b)
    set_operation = tcex.playbook.read(args.set_operation)

    # check for valid inputs
    if set_a is None or set_b is None:
        err = 'Set must not be null.'
        tcex.log.error(err)
        tcex.message_tc(err)
        tcex.exit(1)

    # make input sets
    set_a = set(set_a)
    set_b = set(set_b)

    # log values
    tcex.log.debug('Set A: {}'.format(set_a))
    tcex.log.debug('Set B: {}'.format(set_b))
    tcex.log.info('Set Operation: {}'.format(set_operation))

    result_bool = None
    results = None
    if set_operation == 'Is Subset':
        result_bool = set_a.issubset(set_b)
    elif set_operation == 'Is Superset':
        result_bool = set_a.issuperset(set_b)
    elif set_operation == 'Union':
        results = list(set_a.union(set_b))
    elif set_operation == 'Intersection':
        results = list(set_a.intersection(set_b))
    elif set_operation == 'Difference':
        results = list(set_a.difference(set_b))
    elif set_operation == 'Symmetric Difference':
        results = list(set_a.symmetric_difference(set_b))

    # create output
    tcex.log.debug('Set results: {}'.format(results))
    if result_bool is not None:
        tcex.playbook.create_output('array.set.boolean', str(result_bool).lower())
    if results is not None:
        tcex.playbook.create_output('array.set.count', len(results))
        tcex.playbook.create_output('array.set.results', results)

    tcex.message_tc('{} operation successfully on sets.'.format(set_operation))
    tcex.exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        main_err = 'Generic Error.  See logs for more details ({}).'.format(e)
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(main_err)
        tcex.playbook.exit(1)
