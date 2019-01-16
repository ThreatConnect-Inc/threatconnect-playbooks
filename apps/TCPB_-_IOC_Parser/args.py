# -*- coding: utf-8 -*-
""" Auto-generated Playbook Args """

class Args(object):
    """ Playbook Args """

    def __init__(self, parser):
        """ Initialize class properties. """
        parser.add_argument('--text')
        parser.add_argument('--parse_host_from_email_address', action='store_true')
        parser.add_argument('--parse_address_from_cidr', action='store_true')
        parser.add_argument('--parse_host_from_url', action='store_true')
