#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

###
# Project          : Tact
# FileName         : core.py
# -----------------------------------------------------------------------------
# Author           : Nicolas Deutschmann
# E-Mail           : nicolas.deutschmann@abase.fr
##

import logging

from tact import util

# Logger
LOG = logging.getLogger(__name__)
# Exe dir
exe_dir = util.get_exe_dir()


# -----------------------------------------------------------------------------
#
# AddressBook class
#
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#
# Contact class
#
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#
# Exceptions
#
# -----------------------------------------------------------------------------
class ContactError(Exception):
    pass


class AddressBook(Exception):
    pass


# EOF
