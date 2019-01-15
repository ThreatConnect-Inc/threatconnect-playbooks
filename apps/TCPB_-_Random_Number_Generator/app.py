# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

import random

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """ Playbook App """

    def run(self):
        """  Run the App main logic.

        This method should contain the core logic of the App.
        """
        lower_bound = int(self.tcex.playbook.read(self.args.min_rand))
        upper_bound = int(self.tcex.playbook.read(self.args.max_rand))

        self.tcex.playbook.create_output('random.integer', str(random.randint(lower_bound, upper_bound)), 'String')
        self.tcex.playbook.create_output('random.floatingPoint', str(random.random()), 'String')

        # set the App exit message
        self.exit_message = 'Random numbers created'
