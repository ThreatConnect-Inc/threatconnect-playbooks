# -*- coding: utf-8 -*-
# Arguments
"""Playbook Args"""


class Args:
    """Playbook Args"""

    def __init__(self, parser):
        """Initialize class properties."""

        parser.add_argument('--additional_outputs')
        parser.add_argument('--expression')
        parser.add_argument('--loop_expression')
        parser.add_argument('--loop_expressions')
        parser.add_argument('--loop_variables')
        parser.add_argument('--outputs')
        parser.add_argument('--return_none_on_failure', action='store_true')
        parser.add_argument('--tc_action')
        parser.add_argument('--variables')
