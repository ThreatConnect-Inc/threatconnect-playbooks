# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

import itertools

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        message = self.tcex.playbook.read(self.args.message)
        key = self.tcex.playbook.read(self.args.key)

        output = "".join(chr(ord(a) ^ ord(b)) for a, b in zip(message, itertools.cycle(key)))
        self.tcex.playbook.create_output('xor.output', output, 'String')
