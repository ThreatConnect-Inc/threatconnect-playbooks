# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

import json

from alertaclient.api import Client

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    @staticmethod
    def convert_to_json(alert_object_list):
        json_data = []
        for alert_object in alert_object_list:
            json_data.append(json.dumps(alert_object.tabular(fields='summary', timezone='UTC')))
        return json_data

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        alerta_api_key = self.tcex.playbook.read(self.args.alerta_api_key)
        alerta_api_endpoint = self.tcex.playbook.read(self.args.alerta_api_endpoint)
        alert_id = self.tcex.playbook.read(self.args.alert_id)
        query = self.tcex.playbook.read(self.args.query, True)

        # initialize alerta client
        client = Client(endpoint=alerta_api_endpoint, key=alerta_api_key)

        if not alert_id and not query:
            self.tcex.log.info('Retrieving all alerts from {}'.format(alerta_api_endpoint))
            alerts = client.get_alerts()
        elif alert_id:
            self.tcex.log.info('Retrieving alert with id "{}"'.format(alert_id))
            alerts = [client.get_alert(alert_id)]
        elif query:
            raise NotImplementedError('The ability to search for a query is not implemented yet. If you need it, create an issue here: https://github.com/ThreatConnect-Inc/threatconnect-playbooks/issues')
            # TODO: the difficulty here is that the query should be a tuple (I think) and I'm not sure how to (elegantly) convert the incoming string to a tuple
            # self.tcex.log.info('Retrieving alerts matching the query: {}'.format(query))
            # alerts = client.search(query)

        alerts_json = self.convert_to_json(alerts)

        self.tcex.playbook.create_output('alerta.alerts', alerts_json, 'StringArray')
        self.tcex.playbook.create_output('alerta.alerts.0', alerts_json[0], 'String')
        self.tcex.playbook.create_output('alerta.alertCount', len(alerts_json), 'String')
