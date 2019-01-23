# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

from langdetect import detect_langs

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        text = self.tcex.playbook.read(self.args.text)

        detected_language_code = detect_langs(text)[0].lang
        detected_language_probability = detect_langs(text)[0].prob

        self.tcex.playbook.create_output('detectedLanguageCode', detected_language_code, 'String')
        self.tcex.playbook.create_output('detectedLanguageProbability', detected_language_probability, 'String')
        self.exit_message = 'Detected the language as {} (with a probability of {})'.format(detected_language_code, detected_language_probability)
