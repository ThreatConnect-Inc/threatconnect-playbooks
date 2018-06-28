#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os


def test_playbook_format():
    """Make sure each of the playbooks are valid json."""
    for path, dirs, files in os.walk(os.path.abspath(os.path.join(os.path.dirname(__file__), "../playbooks"))):
        for file_ in files:
            if file_.endswith('.pbx'):
                with open(os.path.join(path, file_), 'r') as f:
                    playbook_file_text = f.read()
                    try:
                        json.loads(playbook_file_text)
                    except json.decoder.JSONDecodeError as e:
                        print("Error reading {}".format(os.path.join(path, file_)))
                        raise e
