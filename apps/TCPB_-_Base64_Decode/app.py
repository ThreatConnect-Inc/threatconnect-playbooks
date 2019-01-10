# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

import base64

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        string = self.tcex.playbook.read(self.args.string)

        decoded_string = base64.b64decode(string).decode('latin-1')

        self.tcex.playbook.create_output('base64.decodedString', decoded_string)

        # set the App exit message
        self.exit_message = 'Base64 decoded'
