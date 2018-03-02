import json
from setuptools import setup, find_packages

with open('install.json', 'r') as fh:
    version = json.load(fh)['programVersion']

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    author='Floyd Hightower',
    description="Fang (see https://ioc-fang.github.io/ for more info. on what it means to 'fang' an indicator) indicators of compromise in text.",
    name='indicator_fanger',
    packages=find_packages(),
    version=version
)
