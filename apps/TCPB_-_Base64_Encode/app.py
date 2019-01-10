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

        encoded_string = base64.b64encode(string.encode('latin-1'))

        self.tcex.playbook.create_output('base64.encodedString', encoded_string)

        # set the App exit message
        self.exit_message = 'Base64 encoded'
