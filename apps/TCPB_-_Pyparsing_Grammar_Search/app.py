# -*- coding: utf-8 -*-
"""ThreatConnect Playbook App"""

from pyparsing import *

# Import default Playbook Class (Required)
from playbook_app import PlaybookApp


class App(PlaybookApp):
    """Playbook App"""

    def run(self):
        """Run the App main logic.

        This method should contain the core logic of the App.
        """
        string = self.tcex.playbook.read(self.args.string)
        grammar_string = self.tcex.playbook.read(self.args.grammar)
        grammar = eval(grammar_string)

        results = grammar.searchString(string).asList()
        results_string = str(results)

        self.tcex.playbook.create_output('pyparser.output', results_string, 'String')
