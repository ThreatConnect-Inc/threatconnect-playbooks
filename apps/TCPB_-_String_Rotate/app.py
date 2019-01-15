# -*- coding: utf-8 -*-
""" ThreatConnect Playbook App """

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """ Playbook App """

    def run(self):
        """  Run the App main logic.

        This method should contain the core logic of the App.
        """
        string = self.tcex.playbook.read(self.args.string)

        try:
            rotation = int(self.tcex.playbook.read(self.args.rotation))
        except ValueError:
            message = 'The rotation number be an integer (the given rotation was: {})'.format(rotation)
            self.exit_message = message
            self.tcex.log.critical(message)
            self.tcex.exit(1, message)

        d = {}
        for c in (65, 97):
            for i in range(26):
                d[chr(i+c)] = chr((i+rotation) % 26 + c)

        self.tcex.playbook.create_output('rotatedString', "".join([d.get(c, c) for c in string]), 'String')

        # set the App exit message
        self.exit_message = 'String rotated'
