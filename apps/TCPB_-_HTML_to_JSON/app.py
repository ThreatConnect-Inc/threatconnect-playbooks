# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

import html_to_json

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        html_string = self.tcex.playbook.read(self.args.html_string)
        convert_tables = self.args.convert_tables

        if convert_tables:
            output_json = html_to_json.convert_tables(html_string)
        else:
            output_json = html_to_json.convert(html_string)

        self.tcex.playbook.create_output('htmlToJson.json', output_json, 'String')
        self.exit_message = 'HTML converted to JSON!'
