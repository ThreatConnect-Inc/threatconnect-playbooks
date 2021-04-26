# -*- coding: utf-8 -*-
# Arguments
"""Application Args"""


class Args:
    """Application Args"""

    def __init__(self, parser):
        """Initialize class properties."""

        parser.add_argument('--additional_outputs')
        parser.add_argument('--binary_array_outputs')
        parser.add_argument('--binary_outputs')
        parser.add_argument('--expression')
        parser.add_argument('--kv_array_outputs')
        parser.add_argument('--kv_outputs')
        parser.add_argument('--loop_expression')
        parser.add_argument('--loop_expressions')
        parser.add_argument('--loop_variables')
        parser.add_argument('--outputs')
        parser.add_argument('--return_none_on_failure', action='store_true')
        parser.add_argument('--tc_action')
        parser.add_argument('--tce_array_outputs')
        parser.add_argument('--tce_outputs')
        parser.add_argument('--tcee_array_outputs')
        parser.add_argument('--tcee_outputs')
        parser.add_argument('--variables')
