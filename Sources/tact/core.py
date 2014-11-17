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
import re

from tact import util
from tact.model import DatabaseManager

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

    def __init__(self, name):
        """ Initialisation """
        self.name = name
        self.book = []

    def find_contact(self, firstname, lastname):
        """ Find a contact in AddressBook (if the contact exist) """
        search_contact = None
        tmp_contact = Contact(firstname, lastname)

        for contact in self.book:
            if contact == tmp_contact:
                search_contact = contact
                break

        return search_contact

    def append_contact(self, contact):
        """ Add a contact directly into AddressBook without any check. """
        self.book.append(contact)

    def add_contact(
            self,
            firstname, lastname,
            mailing_address="", emails=[], phones=[]):
        """ Add a new contact in address book. """
        new_contact = Contact(
            firstname, lastname, mailing_address, emails, phones)
        self.book.append(new_contact)

        return new_contact

    def get_nb_contacts(self):
        """ Get the number of contact in the address book. """
        return len(self.book)

    def remove_contact(self, firstname, lastname,):
        contact = self.find_contact(firstname, lastname)
        if contact:
            self.book.remove(contact)

    def add_contact_phone(self, firstname, lastname, phone):
        contact = self.find_contact(firstname, lastname)
        if contact:
            contact.add_phone(phone)

    def remove_contact_phone(self, firstname, lastname, phone):
        contact = self.find_contact(firstname, lastname)
        if contact:
            contact.remove_phone(phone)

    def add_contact_email(self, firstname, lastname, email):
        contact = self.find_contact(firstname, lastname)
        if contact:
            contact.add_email(email)

    def remove_contact_email(self, firstname, lastname, email):
        contact = self.find_contact(firstname, lastname)
        if contact:
            contact.remove_email(email)

    def __repr__(self):
        return "<AddressBook {} >" .format(self.book)


# -----------------------------------------------------------------------------
#
# AddressBookManager class
#
# -----------------------------------------------------------------------------
class AddressBookManager:

    """ This manager will load and save data into SQLite database and/or
    a CSV file to store and/or export the
    list of contacts contained into the address book. """

    DATA_DIR = os.path.join(exe_dir, 'data')
    DATABASE = os.path.join(exe_dir, DATA_DIR, 'tact.db')
    CSV_DATA_HEADER = [
        'Firstname',
        'Lastname',
        'Home Address',
        'Emails',
        'Phones']

    @staticmethod
    def make(address_book_name="default"):
        """ Build an AddressBook and return data from existing database. """
        address_book = AddressBook(address_book_name)
        database_manager = DatabaseManager(AddressBookManager.DATABASE)

        database_manager.load_data(address_book)

        return address_book

    @staticmethod
    def save(address_book):
        """ Save data from address book in database. """
        database_manager = DatabaseManager(AddressBookManager.DATABASE)
        database_manager.save_data(address_book)

    @staticmethod
    def import_csv(address_book, filepath):
        """ Import data from a CSV file into an address book. """
        if os.path.exists(filepath):
            with open(filepath, newline='') as csv_data:
                reader = csv.reader(
                    csv_data, delimiter=';', quoting=csv.QUOTE_ALL)

                # Skip header
                next(reader)

                for line in reader:
                    contact = ContactFactory.make_contact(line)
                    address_book.append_contact(contact)
        else:
            LOG.error("There is no CSV file to import contact from.")

        return address_book

    @staticmethod
    def export_csv(address_book, filepath):
        """ Export the current address book into a CSV file. """
        contact_data = [
            contact.export_data() for contact in address_book.book]

        book_data = [AddressBookManager.CSV_DATA_HEADER] \
            + contact_data

        with open(filepath, 'w', newline='') as data:
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
        self.phones = [
            phone for phone in phones if ContactChecker.check_phone(phone)]
        self.emails = [
            email for email in emails if ContactChecker.check_email(email)]

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
        if new_phone and \
                ContactChecker.check_phone(new_phone) and \
                new_phone not in self.phones:
            self.phones.append(new_phone)

    def remove_phone(self, old_phone):
        """ remove the old_phone number in the list of phones of the contact.
        if this number exist """
        if old_phone in self.phones:
            self.phones.remove(old_phone)

    def add_email(self, new_email):
        """ Add the new_email in the list of emails of the contact. """
        if new_email and \
                ContactChecker.check_email(new_email) and \
                new_email not in self.emails:
            self.emails.append(new_email)

    def remove_email(self, old_email):
        """ remove the old_email address in the list of emails of the contact.
        if this email exist """
        if old_email in self.emails:
            self.emails.remove(old_email)

    def __eq__(self, other):
        return (
            self.firstname == other.firstname
            and self.lastname == other.lastname)

    def __str__(self):
        to_display = "{} {}\n".format(self.firstname, self.lastname)
        if self.mailing_address:
            to_display += "{}\n".format(self.mailing_address)
        for email in self.emails:
            to_display += "{}\n".format(email)
        for phone in self.phones:
            to_display += "{}\n".format(phone)

        return to_display

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
        if data[3]:
            emails = data[3].split('|')
        else:
            emails = []
        if data[4]:
            phones = data[4].split('|')
        else:
            phones = []

        return Contact(firstname, lastname, mailing_address, emails, phones)


# -----------------------------------------------------------------------------
#
# ContactChecker class
#
# -----------------------------------------------------------------------------
class ContactChecker:

    """ Check attribute's format for a Contact. """

    PHONE_RE = r"^0[0-9]([ .-]?[0-9]{2}){4}$"
    EMAIL_RE = r"^[A-Za-z1-9]+@[a-z]+[.][a-z]+$"

    @staticmethod
    def check_phone(phone):
        """ Check if a phone number has the right format. """
        check = True

        if re.search(ContactChecker.PHONE_RE, phone) is None:
            check = False
            LOG.error("{} is not a phone number.".format(phone))

        return check

    @staticmethod
    def check_email(email):
        """ Check if an email address has the right format. """
        check = True

        if re.search(ContactChecker.EMAIL_RE, email) is None:
            check = False
            LOG.error("{} is not a correct email address.".format(email))

        return check


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
