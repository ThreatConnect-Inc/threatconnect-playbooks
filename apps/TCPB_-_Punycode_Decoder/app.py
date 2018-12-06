# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        action = self.tcex.playbook.read(self.args.action)
        domain = self.tcex.playbook.read(self.args.domain)

        if action == 'decode':
            self.updated_domain = domain.encode('idna').decode('utf-8')
        elif action == 'encode':
            self.updated_domain = domain.encode('utf-8').decode('idna')
        self.exit_message = '{} has been {}ed to {}'.format(domain, action, self.updated_domain)

    def write_output(self):
        """Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.
        """
        self.tcex.log.info('Writing Output')

        action = self.tcex.playbook.read(self.args.action)
        if action == 'decode':
            self.tcex.playbook.create_output('decodedDomain', self.updated_domain)
        else:
            self.tcex.playbook.create_output('encodedDomain', self.updated_domain)
