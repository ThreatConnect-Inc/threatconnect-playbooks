# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        input_string = self.tcex.playbook.read(self.args.string)
        hex_string = '0x'
        for char in input_string:
            hex_string += str(hex(ord(char))).split('x')[-1]
        self.tcex.playbook.create_output('hex', hex_string, 'String')
