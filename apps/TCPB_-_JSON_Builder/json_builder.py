# -*- coding: utf-8 -*-
""" JSON Builder Playbook App """
import json
import traceback
import sys

from tcex import TcEx

# Python 2 unicode
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

tcex = TcEx()

# App args
tcex.parser.add_argument('--json_data', required=True)
args = tcex.args


def main():
    """Main App Logic"""
    json_data = tcex.playbook.read(args.json_data)

    try:
        json.loads(json_data)
    except Exception as e:
        err = 'JSON data was not properly formatted ({}).'.format(e)
        tcex.log.error(err)
        tcex.message_tc(err)
        tcex.playbook.exit(1)

    # create output
    tcex.log.info('JSON data: {}'.format(json_data))
    tcex.playbook.create_output('json.data', json_data)

    tcex.message_tc('JSON data has been created.')
    tcex.exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        main_err = 'Generic Error.  See logs for more details ({}).'.format(e)
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(main_err)
        tcex.playbook.exit(1)
