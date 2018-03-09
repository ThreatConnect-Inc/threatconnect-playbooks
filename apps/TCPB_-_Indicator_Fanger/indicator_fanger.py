# -*- coding: utf-8 -*-
"""Fang (see https://ioc-fang.github.io/ for more info. on what it means to 'fang' an indicator) indicators of compromise in text.."""

import traceback

from tcex import TcEx
import ioc_fanger


def parse_arguments():
    """Parse arguments coming into the app."""
    # retrieve the string as an argument
    tcex.parser.add_argument('--text', help='Text', required=True)
    return tcex.args


def main():
    """."""
    args = parse_arguments()
    text = tcex.playbook.read(args.text)
    tcex.log.info('Text before fanging: {}'.format(text))

    fanged_text = ioc_fanger.fang(text)
    # output the reversed string to downstream playbook apps
    tcex.playbook.create_output('fangedText', fanged_text)
    tcex.log.info('Text after fanging: {}'.format(fanged_text))
    tcex.exit(0)


if __name__ == "__main__":
    # initialize a TcEx instance
    tcex = TcEx()
    try:
        # start the app
        main()
    except SystemExit:
        pass
    except Exception as e:  # if there are any strange errors, log it to the logging in the UI
        err = 'Generic Error.  See logs for more details ({}).'.format(e)
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(err)
        tcex.playbook.exit(1)
