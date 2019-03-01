# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

from ioc_finder import find_iocs

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        text = self.tcex.playbook.read(self.args.text)
        parse_host_from_url = self.args.parse_host_from_url
        parse_host_from_email_address = self.args.parse_host_from_email_address
        parse_address_from_cidr = self.args.parse_address_from_cidr

        self.iocs = find_iocs(text, parse_host_from_url=parse_host_from_url, parse_host_from_email=parse_host_from_email_address, parse_address_from_cidr=parse_address_from_cidr)

        self.exit_message = 'IOCs parsed!'

    def write_output(self):
        """Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.
        """
        self.tcex.playbook.create_output('iocParser.asns', self.iocs['asns'], 'StringArray') 
        self.tcex.playbook.create_output('iocParser.bitcoinAddresses', self.iocs['bitcoin_addresses'], 'StringArray') 
        self.tcex.playbook.create_output('iocParser.cves', self.iocs['cves'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.domains', self.iocs['domains'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.emailAddresses', self.iocs['email_addresses'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.googleAdsensePublisherIds', self.iocs['google_adsense_publisher_ids'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.googleAnalyticsIds', self.iocs['google_analytics_tracker_ids'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.ipv4Cidrs', self.iocs['ipv4_cidrs'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.ipv4s', self.iocs['ipv4s'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.ipv6s', self.iocs['ipv6s'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.md5s', self.iocs['md5s'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.registryKeyPaths', self.iocs['registry_key_paths'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.sha1s', self.iocs['sha1s'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.sha256s', self.iocs['sha256s'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.sha512s', self.iocs['sha512s'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.simpleEmailAddresses', self.iocs['simple_email_addresses'], 'StringArray')
        self.tcex.playbook.create_output('iocParser.urls', self.iocs['urls'], 'StringArray')
