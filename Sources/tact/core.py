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
        search_contact = None
        tmp_contact = Contact(firstname, lastname)

        for contact in self.book:
            if contact == tmp_contact:
                search_contact = contact
                break

        if not search_contact:
            LOG.warn(
                "Contact {} {} doesn't exist.".format(
                    firstname, lastname))

        return search_contact

    def append_contact(self, contact):
        """ Add a contact directly into AddressBook without any check. """
        self.book.append(contact)

    def add_contact(
            self,
            firstname, lastname,
            mailing_address="", emails=[], phones=[]):
        """ Add a new contact in address book. """
        if not self.find_contact(firstname, lastname):
            new_contact = Contact(
                firstname, lastname,
                mailing_address, emails, phones)
            self.book.append(new_contact)
            LOG.info(
                "A new contact has been added in Address Book: {} ".format(
                    new_contact))
        else:
            LOG.info(
                "Contact {} {} already exists in AddressBook.".format(
                    firstname, lastname))

    def get_nb_contacts(self):
        """ Get the number of contact in the address book. """
        return len(self.book)

    def export_data(self):
        """ Export data as a list of lists. """
        data = []
        for contact in self.book:
            data.append(contact.export_data())

        return data

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
                    address_book.append_contact(contact)
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
        if new_phone and ContactChecker.check_phone(new_phone):
            self.phones.append(new_phone)

    def remove_phone(self, old_phone):
        """ remove the old_phone number in the list of phones of the contact.
        if this number exist """
        if old_phone in self.phones:
            self.phones.remove(old_phone)

    def add_email(self, new_email):
        """ Add the new_email in the list of emails of the contact. """
        if new_email and ContactChecker.check_email(new_email):
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
