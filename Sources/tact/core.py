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

    """ Create a address book and add the create contact. """

    def __init__(self):
        """ Initialisation """
        self.book = []

    def add_contact(self, ctact):
        """ Add a new contact in address book. """
        self.book.append(ctact)

    def get_nb_contacts(self):
        """ Get the number of contact in the address book. """
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

        """ Initialisation """

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
