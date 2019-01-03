# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

import ipaddress

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """ Playbook App """

    def run(self):
        """  Run the App main logic.

        This method should contain the core logic of the App.
        """
        cidr_range_string = self.tcex.playbook.read(self.args.cidr_range)
        self.cidr = ipaddress.ip_network(cidr_range_string)

        # set the App exit message
        self.exit_message = 'CIDR Range details gathered and delivered.'

    def write_output(self):
        """ Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.
        """
        self.tcex.log.info('Writing Output')
        self.tcex.playbook.create_output('cidr.addressCount', self.cidr.num_addresses, 'String')
        self.tcex.playbook.create_output('cidr.rangeString', '{} - {}'.format(self.cidr.network_address, self.cidr.broadcast_address), 'String')
        self.tcex.playbook.create_output('cidr.broadcastAddress', self.cidr.broadcast_address, 'String')
        self.tcex.playbook.create_output('cidr.hostmask', self.cidr.hostmask, 'String')
        self.tcex.playbook.create_output('cidr.netmask', self.cidr.netmask, 'String')
