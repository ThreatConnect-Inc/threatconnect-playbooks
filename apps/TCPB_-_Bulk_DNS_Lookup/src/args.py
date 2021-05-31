# Arguments
"""Application Args"""


class Args:
    """Application Args"""

    def __init__(self, parser):
        """Initialize class properties."""

        parser.add_argument('--dns_servers')
        parser.add_argument('--questions')
        parser.add_argument('--rate_limit')
        parser.add_argument('--record_types')
        parser.add_argument('--tc_action')
        parser.add_argument('--transform_ptr', action='store_true')
