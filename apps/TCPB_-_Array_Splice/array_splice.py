# -*- coding: utf-8 -*-
""" Array Splice Playbook App """
import traceback
import sys

from tcex import TcEx

# Python 2 unicode
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

tcex = TcEx()

# App args
tcex.parser.add_argument('--array', required=True)
tcex.parser.add_argument('--splice_start', required=False)
tcex.parser.add_argument('--splice_end', required=False)
tcex.parser.add_argument('--splice_step', required=False)
args = tcex.args


def main():
    """Main App Logic"""
    array = tcex.playbook.read(args.array)
    array_type = tcex.playbook.variable_type(args.array)
    splice_start = tcex.playbook.read(args.splice_start)
    splice_end = tcex.playbook.read(args.splice_end)
    splice_step = tcex.playbook.read(args.splice_step)

    # check for valid inputs
    if array is None:
        err = 'Array must not be null.'
        tcex.log.error(err)
        tcex.message_tc(err)
        tcex.exit(1)

    # splice start
    if splice_start is not None:
        splice_start = int(splice_start)

    # splice end
    if splice_end is not None:
        splice_end = int(splice_end)

    # splice step
    if splice_step is not None:
        splice_step = int(splice_step)

    # build splice pattern
    slice_pattern = slice(splice_start, splice_end, splice_step)

    # log values
    tcex.log.debug('String Array: {}'.format(array))
    tcex.log.info('Splice Start: {}'.format(splice_start))
    tcex.log.info('Splice End: {}'.format(splice_end))
    tcex.log.info('Splice Step: {}'.format(splice_step))

    # create output
    results = array[slice_pattern]
    tcex.log.debug('Results: {}'.format(results))
    tcex.playbook.create_output('array.splice.count', len(results))
    tcex.playbook.create_output('array.splice.results', results, array_type)

    tcex.message_tc('{} items returned by splice.'.format(len(results)))
    tcex.exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        main_err = 'Generic Error.  See logs for more details ({}).'.format(e)
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(main_err)
        tcex.playbook.exit(1)
