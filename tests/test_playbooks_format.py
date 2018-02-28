#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os


def test_playbook_valid_json():
    """Make sure each of the playbooks are valid json."""
    json_errors = 0
    missing_description_errors = 0

    for path, dirs, files in os.walk(os.path.abspath(os.path.join(os.path.dirname(__file__), "../playbooks"))):
        for file_ in files:
            if file_.endswith('.pbx'):
                with open(os.path.join(path, file_), 'r') as f:
                    playbook_file_text = f.read()
                    try:
                        playbook_json = json.loads(playbook_file_text)
                    except json.decoder.JSONDecodeError:
                        json_errors += 1
                        print("Invalid json in {}".format(os.path.join(path, file_)))
                    else:
                        # check to make sure there is a description in the playbook
                        if playbook_json.get('description') == None:
                            missing_description_errors += 1
                            print("No description in {}".format(os.path.join(path, file_)))

    assert json_errors == 0
    assert missing_description_errors == 0


def test_playbook_readme():
    """Make sure each playbook and playbook app has a readme.md."""
    app_errors = 0
    playbook_errors = 0

    for path, dirs, files in os.walk(os.path.abspath(os.path.join(os.path.dirname(__file__), "../apps"))):
        # only check for a readme if there are files and if the directory is a tc playbook app
        if len(files) > 0 and path.split('/')[-1].startswith('TCPB'):
            lower_cased_file_names = [file_.lower() for file_ in files]
            try:
                assert 'readme.md' in lower_cased_file_names
            except AssertionError:
                app_errors += 1
                print("No README.md file in {}".format(path))
        # stop after going through the top level of each playbook's directory
        break

    for path, dirs, files in os.walk(os.path.abspath(os.path.join(os.path.dirname(__file__), "../playbooks"))):
        if len(files) > 0:
            lower_cased_file_names = [file_.lower() for file_ in files]
            try:
                assert 'readme.md' in lower_cased_file_names
            except AssertionError:
                playbook_errors += 1
                print("No README.md file in {}".format(path))
        # stop after going through the top level of each playbook's directory
        break

    assert app_errors == 0
    assert playbook_errors == 0
