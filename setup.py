from setuptools import setup, find_packages
from glob import glob
import os

NAME = 'PyEventLogViewer'
VERSION = '0.0.1'

SCRIPT_DIR = 'bin'
SCRIPT_GLOB = '*.py*'
scripts = glob(os.path.join(SCRIPT_DIR, SCRIPT_GLOB))
print(scripts)

LIB_DIR = 'winlogtimeline'
PKG_DIR = 'winlogtimeline'
pkgs = ['{root}.{module}'.format(root=PKG_DIR, module=pkg) for pkg in find_packages(where=LIB_DIR)]


setup(
    name=NAME,
    version=VERSION,
    packages=pkgs,
    package_data={
        'winlogtimeline.ui': ['icons/*']
    },
    scripts=scripts,
    data_files=[
        ('config', ['config/config.json'])
    ],
)
