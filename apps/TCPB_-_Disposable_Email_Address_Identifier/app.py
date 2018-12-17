# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

import requests

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp

DISPOSABLE_EMAIL_DOMAINS_ENDPOINT = 'https://raw.githubusercontent.com/martenson/disposable-email-domains/master/disposable_email_blocklist.conf'


class App(PlaybookApp):
    """ Playbook App """

    def _get_disposable_domain_hosts(self):
        disposable_hosts_content = requests.get(DISPOSABLE_EMAIL_DOMAINS_ENDPOINT).text
        return disposable_hosts_content.split('\n')

    def run(self):
        self.disposable_domains = self._get_disposable_domain_hosts()
        input_data = self.tcex.playbook.read(self.args.email_address_or_the_hostname_of_an_email_address)

        # if the input appears to be an email address, get the hostname from the email address (otherwise, we are just assuming it is a host)
        if '@' in input_data:
            input_data = input_data.split('@')[1]

        if input_data in self.disposable_domains:
            self.tcex.playbook.create_output('isDisposableEmailHostname', 1, 'String')
            self.exit_message = '{} is found in the list disposable email service hostnames ({})'.format(input_data, DISPOSABLE_EMAIL_DOMAINS_ENDPOINT)
        else:
            self.tcex.playbook.create_output('isDisposableEmailHostname', 0, 'String')
            self.exit_message = '{} is not found in the list of disposable email service hostnames ({})'.format(input_data, DISPOSABLE_EMAIL_DOMAINS_ENDPOINT)
