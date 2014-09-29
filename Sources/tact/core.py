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

    """ create a address book and add the create contact. """

    def __init__(self):
        """ initialisation """
        self.book = []

    def add_contact(self, ctact):
        """ add a new contact in address book. """
        self.book.append(ctact)

    def get_nb_contacts(self):
        """ get the number of contact in the address book. """
        return len(self.book)


# -----------------------------------------------------------------------------
#
# Contact class
#
# -----------------------------------------------------------------------------
class Contact:

    """ Create a new contact ( firstname and lastname are obligatory and in
        that order ). """

    def __init__(
            self, firstname, lastname, mail_address="", email="", phone=""):

        """ initialisation """

        self.firstname = firstname
        self.lastname = lastname
        self.mail_address = mail_address
        self.email = email
        self.phone = phone


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
