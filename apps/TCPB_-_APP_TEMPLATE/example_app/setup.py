import json
from setuptools import setup, find_packages

with open('install.json', 'r') as fh:
    version = json.load(fh)['programVersion']

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    author=' ',
    description='Example playbook app created using the TcEx package. The app takes a string input and reverses it.',
    name='example_app',
    packages=find_packages(),
    version=version
)
