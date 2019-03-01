# -*- coding: utf-8 -*-
""" Playbook App """
import traceback
import sys

from tcex import TcEx

from app import App


# Python 2 unicode
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

tcex = TcEx()

if __name__ == '__main__':
    try:
        # load App class
        app = App(tcex)

        # parse args
        app.parse_args()

        # perform prep/startup operations
        app.start()

        # run the main logic
        app.run()

        # write requested value for downstream Apps
        app.write_output()

        # perform cleanup operations
        app.done()

        # explicitly call the exit method
        tcex.exit(msg=app.exit_message)

    except Exception as e:
        main_err = 'Generic Error.  See logs for more details ({}).'.format(e)
        tcex.log.error(traceback.format_exc())
        tcex.playbook.exit(1, main_err)
