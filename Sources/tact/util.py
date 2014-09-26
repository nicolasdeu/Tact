#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

###
# Project          : Tact
# FileName         : util.py
# -----------------------------------------------------------------------------
# Author           : Nicolas Deutschmann
# E-Mail           : nicolas.deutschmann@abase.fr
##

import os
import re
import sys
import logging
import logging.config

from codecs import open

# Logger
LOG = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
#
# Module methods
#
# -----------------------------------------------------------------------------
def get_exe_dir():
    """ Gets Executable directory. """
    if 'tact' in os.path.basename(sys.executable).lower():
        exe_dir = os.path.abspath(sys.executable)
    else:
        exe_dir = os.path.abspath('.')

    return exe_dir


def init_logging():
    """ Loads logging configuration file and inits logging system. """
    exe_dir = get_exe_dir()

    # Log directory
    log_dir = os.path.join(exe_dir, 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # Configuration file for logger
    log_file = os.path.join(exe_dir, 'Config', 'logging.conf')
    # Load configuration file
    logging.config.fileConfig(log_file)

    return logging.getLogger("tact")


def find_version():
    """ Finds version of the application in the __init__ file of package. """
    here = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(here, '__init__.py'), encoding='utf-8') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# EOF
