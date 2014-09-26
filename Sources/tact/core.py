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

# Logger
LOG = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
#
# AddressBook class
#
# -----------------------------------------------------------------------------
class AddressBook:

    """docstring for AddressBook"""

    def __init__(self):
        self.book = []

    def add_contact(self, ctact):
        self.book.append(ctact)

    def get_nb_contacts(self):
        return len(self.book)


# -----------------------------------------------------------------------------
#
# Contact class
#
# -----------------------------------------------------------------------------
class Contact:

    """docstring for Contact"""

    def __init__(
            self, fname, lname, mail_address="", email="", ph=""):
        self.firstname = fname
        self.lastname = lname
        mailling_address = mail_address
        e_mailling_address = email
        phone = ph




# -----------------------------------------------------------------------------
#
# Exceptions
#
# -----------------------------------------------------------------------------

class ContactError(Exception):
    pass


class AddressBookError(Exception):
    pass


# EOF
