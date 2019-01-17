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
        string_1 = self.tcex.playbook.read(self.args.string_1)
        string_2 = self.tcex.playbook.read(self.args.string_2)

        if len(string_1) != len(string_2):
            message = 'The length of the two strings must be the same'
            self.exit_message = message
            self.tcex.exit(1, message)

        hamming_distance = sum(el1 != el2 for el1, el2 in zip(string_1, string_2))

        self.tcex.playbook.create_output('hammingDistance', hamming_distance, 'String')
        self.tcex.playbook.create_output('hammingDistance.percentage', round((hamming_distance / len(string_1)) * 100, 2), 'String')
