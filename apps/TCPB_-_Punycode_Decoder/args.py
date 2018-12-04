# -*- coding: utf-8 -*-
"""Playbook Args"""

class Args(object):
    """Playbook Args"""

    def __init__(self, _tcex):
        """Initialize class properties."""
        _tcex.parser.add_argument('--action', choices=['decode', 'encode'], required=True)
        _tcex.parser.add_argument('--domain', required=True)
