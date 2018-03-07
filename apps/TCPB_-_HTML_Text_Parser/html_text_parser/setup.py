import json
from setuptools import setup, find_packages

with open('install.json', 'r') as fh:
    version = json.load(fh)['programVersion']

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    author='Floyd Hightower',
    description='Parse text from html.',
    name='html_text_parser',
    packages=find_packages(),
    version=version
)
