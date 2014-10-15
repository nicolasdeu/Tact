#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

###
# Project          : Tact
# FileName         : core.py
# -----------------------------------------------------------------------------
# Author           : Nicolas Deutschmann
# E-Mail           : nicolas.deutschmann@abase.fr
##

import os
import csv
import logging

from tact import util

# Gets execution directory
exe_dir = util.get_exe_dir()

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

    def find_contact(self, firstname, lastname):
        """ Find a contact in AddressBook (if the contact exist) """
        result = None
        tmp_contact = Contact(firstname, lastname)
        LOG.info(" Address Book {} ".format(self.book))

        for contact in self.book:
            if contact == tmp_contact:
                result = contact
                break

        return result

    def add_contact(self, contact):
        """ Add a new contact in address book. """
        self.book.append(contact)

    def get_nb_contacts(self):
        """ Get the number of contact in the address book. """
        return len(self.book)

    def export_data(self):
        """ Export data as a list of lists. """
        data = []
        for contact in self.book:
            data.append(contact.export_data())

        return data

    def __repr__(self):
        return "<AddressBook {} >" .format(self.book)


# -----------------------------------------------------------------------------
#
# AddressBookManager class
#
# -----------------------------------------------------------------------------
class AddressBookManager:

    """ This manager will load and save data from a CSV file to build/store
    the list of contacts contained into the address book. """

    DATA_DIR = os.path.join(exe_dir, 'data')
    DATA_FILE = os.path.join(DATA_DIR, 'tact.csv')
    DATA_HEADER = ['Firstname', 'Lastname', 'Home Address', 'Emails', 'Phones']

    @staticmethod
    def make_address_book():
        """ Build an AddressBook with data from a CSV file. """
        address_book = AddressBook()

        if os.path.exists(AddressBookManager.DATA_FILE):
            with open(AddressBookManager.DATA_FILE, newline='') as csv_data:
                reader = csv.reader(
                    csv_data, delimiter=';', quoting=csv.QUOTE_ALL)

                # Skip header
                next(reader)

                for line in reader:
                    contact = ContactFactory.make_contact(line)
                    address_book.add_contact(contact)
        else:
            LOG.info(
                "There is no contact previously saved, "
                "this is a brand new address book.")

        return address_book

    @staticmethod
    def save_address_book(address_book):
        """ Save address book on disk into a CSV file. """
        if not os.path.exists(AddressBookManager.DATA_DIR):
            os.mkdir(AddressBookManager.DATA_DIR)

        book_data = [AddressBookManager.DATA_HEADER] \
            + address_book.export_data()

        with open(AddressBookManager.DATA_FILE, 'w', newline='') as data:
            writer = csv.writer(
                data, delimiter=';', quoting=csv.QUOTE_ALL)
            writer.writerows(book_data)


# -----------------------------------------------------------------------------
#
# Contact class
#
# -----------------------------------------------------------------------------
class Contact:

    """ Create a new contact (firstname and lastname are obligatory and in
        that order). """

    def __init__(
            self,
            firstname, lastname, mailing_address="", emails=[], phones=[]):
        """ Initialisation """

        self.firstname = firstname
        self.lastname = lastname
        self.mailing_address = mailing_address
        self.emails = emails
        self.phones = phones

    def export_data(self):
        """ Export data as a list. """
        return [
            self.firstname,
            self.lastname,
            self.mailing_address,
            "|".join(self.emails),
            "|".join(self.phones)
        ]

    def add_phone(self, new_phone):
        """ Add the new_phone number in the list of phones of the contact. """
        self.phones.append(new_phone)

    def remove_phone(self, old_phone):
        """ remove the old_phone number in the list of phones of the contact.
        if this number exist """
        for phone in self.phones:
            if phone == old_phone:
                self.phones.remove(phone)

    def add_email(self, new_email):
        """ Add the new_email in the list of emails of the contact. """
        self.email.append(new_email)

    def remove_email(self, old_email):
        """ remove the old_email address in the list of emails of the contact.
        if this email exist """
        for email in self.emails:
            if email == old_email:
                self.emails.remove(email)

    def __eq__(self, other):
        return (
            self.firstname == other.firstname
            and self.lastname == other.lastname)

    def __repr__(self):
        return "<Contact {} {} >".format(self.firstname, self.lastname)


# -----------------------------------------------------------------------------
#
# ContactFactory class
#
# -----------------------------------------------------------------------------
class ContactFactory:

    """ Build contact object. """

    @staticmethod
    def make_contact(data):
        """ Create a Contact instance thanks to raw data. """
        firstname = data[0]
        lastname = data[1]
        mailing_address = data[2]
        emails = data[3].split('|')
        phones = data[4].split('|')

        return Contact(firstname, lastname, mailing_address, emails, phones)


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
