"""Playbook App"""
# standard library
import os
import traceback

# first-party
from app_lib import AppLib


# pylint: disable=no-member
def run() -> None:
    """Update path and run the App."""
    # update the path to ensure the App has access to required modules
    app_lib = AppLib()
    app_lib.update_path()

    # import modules after path has been updated

    # third-party
    from tcex import TcEx  # pylint: disable=import-outside-toplevel

    # first-party
    from app import App  # pylint: disable=import-outside-toplevel

    config_file = os.environ.get('TCEX_APP_CONFIG_DEV')
    if config_file:
        if not os.path.isfile(config_file):
            raise RuntimeError(f'Missing {config_file} config file.')

    tcex = TcEx(config_file=config_file)

    try:
        # load App class
        app = App(tcex)

        # perform prep/setup operations
        app.setup(**{})

        # run the App logic
        if hasattr(app.inputs.model, 'tc_action') and app.inputs.model.tc_action is not None:
            # if the args NameSpace has the reserved arg of "tc_action", this arg value is used to
            # triggers a call to the app.<tc_action>() method.  an exact match to the method is
            # tried first, followed by a normalization of the tc_action value, and finally an
            # attempt is made to find the reserved "tc_action_map" property to map value to method.
            tc_action: str = app.inputs.model.tc_action
            tc_action_formatted: str = tc_action.lower().replace(' ', '_')
            tc_action_map = 'tc_action_map'  # reserved property name for action to method map

            # run action method
            if hasattr(app, tc_action):
                getattr(app, tc_action)()
            elif hasattr(app, tc_action_formatted):
                getattr(app, tc_action_formatted)()
            elif hasattr(app, tc_action_map):
                app.tc_action_map.get(tc_action)()  # pylint: disable=no-member
            else:
                tcex.exit(1, f'Action method ({app.inputs.model.tc_action}) was not found.')
        else:
            # default to run method
            app.run(**{})

        # write requested value for downstream Apps
        app.write_output()  # pylint: disable=no-member

        # perform cleanup/teardown operations
        app.teardown(**{})

        # explicitly call the exit method
        tcex.exit(msg=app.exit_message)
    except Exception as e:
        main_err = f'Generic Error.  See logs for more details ({e}).'
        tcex.log.error(traceback.format_exc())
        tcex.exit(1, main_err)


if __name__ == '__main__':
    # Run the App
    run()
