# -*- coding: utf-8 -*-
""" Auto-generated Playbook Args """

class Args(object):
    """ Playbook Args """

    def __init__(self, _tcex):
        """ Initialize class properties. """
        _tcex.parser.add_argument('--remove_query_strings', action='store_true')
        _tcex.parser.add_argument('--urls')
        _tcex.parser.add_argument('--remove_fragments', action='store_true')
        _tcex.parser.add_argument('--remove_path', action='store_true')
