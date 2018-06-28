# -*- coding: utf-8 -*-
""" JSON Pretty Playbook App """
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
tcex.parser.add_argument('--indent', default=4)
tcex.parser.add_argument('--json_data', required=True)
tcex.parser.add_argument('--sort_keys', action='store_true')
args = tcex.args


def main():
    """Main App Logic"""
    indent = int(tcex.playbook.read(args.indent))
    json_data = tcex.playbook.read(args.json_data)
    json_data_type = tcex.playbook.variable_type(args.json_data)
    if json_data_type in ['String']:
        json_data = json.loads(json_data)
    pretty_json = json.dumps(json_data, indent=indent, sort_keys=args.sort_keys)
    tcex.playbook.create_output('json.pretty', pretty_json)

    tcex.message_tc('JSON data has been formatted.')
    tcex.exit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        main_err = 'Generic Error.  See logs for more details ({}).'.format(e)
        tcex.log.error(traceback.format_exc())
        tcex.message_tc(main_err)
        tcex.playbook.exit(1)
