# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""
import json

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp

# pylint: disable=attribute-defined-outside-init
class App(PlaybookApp):
    """Playbook App"""

    def __init__(self, _tcex):
        """Initialize class properties.

        This method can be OPTIONALLY overridden.
        """
        super().__init__(_tcex)
        self.all_items = []

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        # read inputs
        indent = int(self.tcex.playbook.read(self.args.indent))
        byte_json_data = self.tcex.playbook.read(self.args.json_data)

        json_string = byte_json_data.decode()
        json_data = json.loads(json_string)

        try:
            # 1. each json_data['alerts'] is an identifier
            for alerts in json_data['alerts']:
                # 2. for each, 'items', add key:identifier name,
                identifier_name = alerts.get("name") 
                for item in alerts.items():
                    for item in alerts['items']:
                        item['source_identifier'] = identifier_name
                        self.all_items.append({'key': item['id'], 'value': item})

        except Exception:
            self.tcex.exit(1, 'Failed parsing JSON data.')

        # set the App exit message
        self.exit_message = 'Firework Alert Ingested.'


    def write_output(self):
        """Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.json_data = self.tcex.playbook.read(self.args.json_data)
        """
        self.tcex.log.info('Writing Output')
        self.tcex.log.info(type(self.all_items))
        self.tcex.log.info(len(self.all_items))
        self.tcex.playbook.create_output('firework_alert.json', self.all_items)
