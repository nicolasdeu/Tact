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

    def import_data(self, data):
        self.book = data

    def find_contact(self, firstname, lastname):
        """ Find a contact in AddressBook (if the contact exist) """
        for contact in (self.book):
            if firstname == contact[0] and lastname == contact[1]:
                return contact

    def add_contact(self, ctact):
        """ Add a new contact in address book. """
        self.book.append(ctact)

    def get_nb_contacts(self):
        """ Get the number of contact in the address book. """
        return len(self.book)

    def export_data(self):

        data = []
        for contact in self.book:
            for parametre in contact:
                if type(parametre) == list:
                    parametre = "|".join(parametre)

        return data

    def _repr_(self):
        return ("<address book contain {} >" .format(self.ctact))


# -----------------------------------------------------------------------------
#
# Contact class
#
# -----------------------------------------------------------------------------
class Contact:

    """ Create a new contact ( firstname and lastname are obligatory and in
        that order ). """

    def __init__(
            self,
            firstname, lastname, mailing_address="", emails=[], phones=[]):
        """ Initialisation """

        self.firstname = firstname
        self.lastname = lastname
        self.mailing_address = mailing_address
        self.emails = emails
        self.phones = phones

    def _repr_(self):
        return ("contact add {} {} ".format(self.firstname, self.lastname))


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
