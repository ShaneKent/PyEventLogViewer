from setuptools import setup, find_packages
from glob import glob
from itertools import chain
import os.path

"""Setup configuration values"""
# Package metadata
NAME = 'PyEventLogViewer'
VERSION = '1.0.0'
URL = 'https://github.com/ShaneKent/PyEventLogViewer'
AUTHOR = 'Redacted Capstone Team'
AUTHOR_EMAIL = 'pyeventlogviewer@gmail.com'
# The name of the folder that packages are located in
LIB_DIR = 'winlogtimeline'          # I'd prefer this to be lib, but PyCharm has issues with that - C 10/3/17
# The name of the package to ship all packages under
PKG_DIR = 'winlogtimeline'
# Any data files/folders needed by packages
PACKAGE_DATA = {
    'ui': ['icons/*'],              # Icons needed to ship the GUI
    'util': ['config/*'],           # Location of the application configuration file
}
# The location of script files.
SCRIPT_DIR = 'bin'
# The glob for identifying script files
SCRIPT_GLOBS = ['*.py', '*.pyw']

DEPENDENCIES = ['libevtx-python',
                'appdirs',
                'xmltodict']

SETUP_DEPENDENCIES = ['pytest-runner']

TEST_DEPENDENCIES = ['pytest']

SUPPORTED_VERSIONS = '>=3.6'

"""Automated argument formatting and setup call"""
# Grab all of the packages
pkgs = ['{root}.{module}'.format(root=PKG_DIR, module=pkg) for pkg in find_packages(where=LIB_DIR)]
# Place the package data in the proper format
pkg_data = {'{pkg}.{subpkg}'.format(pkg=PKG_DIR, subpkg=key): value for key, value in PACKAGE_DATA.items()}
# Grab all of the scripts matching the glob
script_glob_results = (glob(os.path.join(SCRIPT_DIR, script_glob)) for script_glob in SCRIPT_GLOBS)
# Flatten the list
scripts = list(chain(*script_glob_results))

setup(
    name=NAME,
    version=VERSION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=pkgs,
    package_data=pkg_data,
    scripts=scripts,
    install_requires=DEPENDENCIES,
    setup_requires=SETUP_DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES,
    python_requires=SUPPORTED_VERSIONS
)
