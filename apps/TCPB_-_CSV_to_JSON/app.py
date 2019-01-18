# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

import csv_to_json

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        csv_string = self.tcex.playbook.read(self.args.csv_string)
        delimiter = self.tcex.playbook.read(self.args.delimiter)
        comment_character = self.tcex.playbook.read(self.args.comment_character)
        heading_row = self.tcex.playbook.read(self.args.heading_row)

        output_json = csv_to_json.convert(csv_string, delimiter=delimiter, comment_character=comment_character, heading_row=heading_row)
        self.tcex.playbook.create_output('csvToJson.json', output_json, 'String')

        csv_string = self.tcex.playbook.read(self.args.csv_string)
