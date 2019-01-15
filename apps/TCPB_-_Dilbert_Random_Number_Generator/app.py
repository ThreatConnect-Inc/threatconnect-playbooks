# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """ Playbook App """

    def run(self):
        """  Run the App main logic.

        This method should contain the core logic of the App.
        """
        self.tcex.playbook.create_output('dilbertRandom.integer', '9', 'String')

        # set the App exit message
        self.exit_message = 'Random number created'
