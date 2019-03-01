# -*- coding: utf-8 -*-
""" Auto-generated Playbook Args """

class Args(object):
    """ Playbook Args """

    def __init__(self, parser):
        """ Initialize class properties. """
        parser.add_argument('--alerta_api_key')
        parser.add_argument('--alerta_api_endpoint')
        parser.add_argument('--resource_under_alarm')
        parser.add_argument('--event_name')
        parser.add_argument('--environment', default='Production')
        parser.add_argument('--severity')
        parser.add_argument('--services')
