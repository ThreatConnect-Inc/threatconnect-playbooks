# -*- coding: utf-8 -*-
"""Parse text from html."""

import traceback

from bs4 import BeautifulSoup
from tcex import TcEx


def parse_arguments():
    """Parse arguments coming into the app."""
    tcex.parser.add_argument('--html_input', help='HTML Input', required=True)
    return tcex.args


def main():
    """."""
    args = parse_arguments()

    html = tcex.playbook.read(args.html_input)
    tcex.log.info('HTML Input: {}'.format(html))

    # get the text from the HTML
    text = ''.join(BeautifulSoup(html, "html.parser").findAll(text=True))

    tcex.playbook.create_output('html_parser.text', text)
    tcex.exit(0)


if __name__ == "__main__":
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
