# -*- coding: utf-8 -*-
""" Auto-generated Playbook Args """

class Args(object):
    """ Playbook Args """

    def __init__(self, parser):
        """ Initialize class properties. """
        parser.add_argument('--csv_string')
        parser.add_argument('--delimiter', default=',')
        parser.add_argument('--comment_character', default='#')
        parser.add_argument('--heading_row')
