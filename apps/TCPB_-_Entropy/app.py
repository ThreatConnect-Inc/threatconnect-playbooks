# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

import math

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        ignore_case = self.args.ignore_case
        text = self.tcex.playbook.read(self.args.text)

        if ignore_case:
            text = text.lower()

        # make a deduplicated list of all character codes in the text
        character_code_set = list(set([ord(char) for char in text]))

        if not text:
            entropy = 0
        else:
            entropy = 0

            for char_code in character_code_set:
                p_char = float(text.count(chr(char_code))) / len(text)
                if p_char > 0:
                    entropy += - p_char*math.log(p_char, 2)

        self.tcex.playbook.create_output('entropy', entropy, 'String')
