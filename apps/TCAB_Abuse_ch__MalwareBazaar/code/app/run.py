# -*- coding: utf-8 -*-
"""Playbook App"""
import traceback

from app_lib import AppLib


def run():
    """Update path and run the App."""

    # update the path to ensure the App has access to required modules
    app_lib = AppLib()
    app_lib.update_path()

    # import modules after path has been updated
    from tcex import TcEx
    from app import App

    tcex = TcEx()

    try:
        # load App class
        app = App(tcex)

        # perform prep/setup operations
        app.setup()

        # run the App logic
        if hasattr(app.args, 'tc_action') and app.args.tc_action is not None:
            # if the args NameSpace has the reserved arg of "tc_action", this arg value is used to
            # triggers a call to the app.<tc_action>() method.  an exact match to the method is
            # tried first, followed by a normalization of the tc_action value, and finally an
            # attempt is made to find the reserved "tc_action_map" property to map value to method.
            tc_action = app.args.tc_action
            tc_action_formatted = tc_action.lower().replace(' ', '_')
            tc_action_map = 'tc_action_map'  # reserved property name for action to method map
            # run action method
            if hasattr(app, tc_action):
                getattr(app, tc_action)()
            elif hasattr(app, tc_action_formatted):
                getattr(app, tc_action_formatted)()
            elif hasattr(app, tc_action_map):
                app.tc_action_map.get(app.args.tc_action)()  # pylint: disable=no-member
            else:
                tcex.exit(1, f'Action method ({app.args.tc_action}) was not found.')
        else:
            # default to run method
            app.run()

        # write requested value for downstream Apps
        tcex.playbook.write_output()
        app.write_output()  # pylint: disable=no-member

        # perform cleanup/teardown operations
        app.teardown()

        # explicitly call the exit method
        tcex.playbook.exit(msg=app.exit_message)

    except Exception as e:
        main_err = f'Generic Error.  See logs for more details ({e}).'
        tcex.log.error(traceback.format_exc())
        tcex.playbook.exit(1, main_err)


if __name__ == '__main__':
    # Run the App
    run()
