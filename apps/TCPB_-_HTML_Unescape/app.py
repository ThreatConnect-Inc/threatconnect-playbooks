# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

import html

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """ Playbook App """

    def run(self):
        """  Run the App main logic.

        This method should contain the core logic of the App.
        """
        escaped_html_string = self.tcex.playbook.read(self.args.string)
        self.tcex.playbook.create_output('html.unescaped', html.unescape(escaped_html_string), 'String')

        # set the App exit message
        self.exit_message = 'HTML unescaped'
