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
        # read inputs
        char_codes = self.tcex.playbook.read(self.args.character_codes)

        # convert string input to list
        if self.tcex.playbook.variable_type(self.args.character_codes) == 'String':
            char_codes = char_codes.split(',')

        self.tcex.playbook.create_output('fromCharCode.convertedString', ''.join([chr(int(char_code)) for char_code in char_codes]), 'String')

        # set the App exit message
        self.exit_message = 'Converted character codes into a string.'
