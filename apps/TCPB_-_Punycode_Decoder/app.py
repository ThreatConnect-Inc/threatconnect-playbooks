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
        if self.args.action == 'decode':
            self.updated_domain = self.args.domain.encode('idna').decode('utf-8')
        elif self.args.action == 'encode':
            self.updated_domain = self.args.domain.encode('utf-8').decode('idna')
        self.exit_message = '{} has been {}ed to {}'.format(self.args.domain, self.args.action, self.updated_domain)

    def write_output(self):
        """Write the Playbook output variables.

        This method should be overridden with the output variables defined in the install.json
        configuration file.
        """
        self.tcex.log.info('Writing Output')
        if self.args.action == 'decode':
            self.tcex.playbook.create_output('decodedDomain', self.updated_domain)
        else:
            self.tcex.playbook.create_output('encodedDomain', self.updated_domain)
