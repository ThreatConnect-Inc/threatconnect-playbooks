# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

from alertaclient.api import Client

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        alerta_api_key = self.tcex.playbook.read(self.args.alerta_api_key)
        alerta_api_endpoint = self.tcex.playbook.read(self.args.alerta_api_endpoint)
        resource = self.tcex.playbook.read(self.args.resource_under_alarm)
        event = self.tcex.playbook.read(self.args.event_name)
        severity = self.tcex.playbook.read(self.args.severity)
        service = self.tcex.playbook.read(self.args.services, True)
        environment = self.tcex.playbook.read(self.args.environment)

        # initialize alerta client
        client = Client(endpoint=alerta_api_endpoint, key=alerta_api_key)

        new_alert = client.send_alert(resource, event, severity=severity, environment=environment, service=service)[1]
        self.tcex.playbook.create_output('alerta.alertId', new_alert.id)
