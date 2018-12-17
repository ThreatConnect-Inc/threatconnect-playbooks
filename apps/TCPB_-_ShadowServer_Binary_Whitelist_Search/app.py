# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

import requests

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """ Playbook App """

    def run(self):
        """  Run the App main logic.

        This method should contain the core logic of the App.
        """
        url = 'http://bin-test.shadowserver.org/api?md5={}'
        md5 = self.tcex.playbook.read(self.args.md5_hash)
        self.tcex.log.info('Querying the ShadowServer API for md5: {}'.format(md5))

        response = requests.get(url.format(md5)).text
        response = response.replace(md5, '', 1).strip()
        self.tcex.log.info('Response from ShadowServer API: {}'.format(response))
        self.tcex.playbook.create_output('shadowServerBinaryCheckResponse', response)
