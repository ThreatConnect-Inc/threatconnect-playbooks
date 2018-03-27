# -*- coding: utf-8 -*-
"""Validate a yara rule."""

import traceback

from tcex import TcEx
import yara_validator


def parse_arguments():
    """Parse arguments coming into the app."""
    tcex.parser.add_argument('--yara_rule', help='Yara rule', required=True)
    return tcex.args


def main():
    """."""
    args = parse_arguments()
    yara_rule = tcex.playbook.read(args.yara_rule)
    tcex.log.info('Yara rule: {}'.format(yara_rule))

    validator = yara_validator.YaraValidator()
    validator.add_rule_source(rule)
    valid, broken, repaired = validator.check_all()

    error_data = None
    repaired_source = None

    if valid:
        validation_status = "VALID"
        source = valid[0].source
    elif broken:
        validation_status = "BROKEN"
        source = broken[0].source
        error_data = broken[0].error_data
    elif repaired:
        validation_status = "REPAIRED"
        source = repaired[0].source
        repaired_source = repaired[0].repaired_source
    else:
        validation_status = "UNKNOWN"
        source = ""

    tcex.log.debug('validationStatus: {}'.format(validation_status))
    tcex.log.debug('errorData: {}'.format(error_data))
    tcex.log.debug('repairedSource: {}'.format(repaired_source))
    tcex.log.debug('source: {}'.format(source))

    tcex.playbook.create_output('validationStatus', validation_status)
    tcex.playbook.create_output('errorData', error_data)
    tcex.playbook.create_output('repairedSource', repaired_source)
    tcex.playbook.create_output('source', source)

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
        tcex.exit(1)
