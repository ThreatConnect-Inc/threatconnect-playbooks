# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

import ipaddress

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """ Playbook App """

    @staticmethod
    def _format_ipv6_for_tc(exploded_ipv6):
        address_sections = [section.replace("0000", "xxxx").lstrip("0") for section in exploded_ipv6.split(":")] 
        formatted_address_sections = ":".join(address_sections)
        return formatted_address_sections.replace("xxxx", "0")

    def run(self):
        """  Run the App main logic.

        This method should contain the core logic of the App.
        """
        ip_string = self.tcex.playbook.read(self.args.ip_address)
        self.ip = ipaddress.ip_address(ip_string)

        # set the App exit message
        self.exit_message = 'IP details gathered and delivered.'

    def write_output(self):
        """ Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.
        """
        self.tcex.log.info('Writing Output')
        self.tcex.playbook.create_output('ip.isPrivate', self.ip.is_private, 'String')
        self.tcex.playbook.create_output('ip.version', self.ip.version, 'String')
        self.tcex.playbook.create_output('ip.isReserved', self.ip.is_reserved, 'String')

        if self.ip.version == 6:
            self.tcex.playbook.create_output('ipv6.exploded', self.ip.exploded, 'String')
            self.tcex.playbook.create_output('ipv6.compressed', self.ip.compressed, 'String')
            self.tcex.playbook.create_output('ipv6.threatConnectFormat', self._format_ipv6_for_tc(self.ip.exploded), 'String')
        else:
            self.tcex.playbook.create_output('ipv6.exploded', 'null', 'String')
            self.tcex.playbook.create_output('ipv6.compressed', 'null', 'String')
            self.tcex.playbook.create_output('ipv6.threatConnectFormat', 'null', 'String')
