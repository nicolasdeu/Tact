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
import logging
import re

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker, relationship

from tact import util

# Gets execution directory
exe_dir = util.get_exe_dir()

# Logger
LOG = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
#
# Base
#
# -----------------------------------------------------------------------------
@as_declarative()
class Base(object):

    '''base class with id field'''
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)


# -----------------------------------------------------------------------------
#
# AddressBook class
#
# -----------------------------------------------------------------------------
class AddressBook(Base):

    """ Create a address book and add the create contact. """

    name = Column(String(100), nullable=False)
    contacts = relationship(
        "Contact",
        order_by="Contact.id", cascade="all,delete", backref="addressbook", )

    def __init__(self, name="default"):
        self.name = name

    def find_contact(self, firstname, lastname):
        """ Find a contact in AddressBook (if the contact exist) """
        search_contact = None
        tmp_contact = Contact(firstname, lastname)

        for contact in self.contacts:
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
        self.contacts.append(contact)

    def add_contact(
            self,
            firstname, lastname,
            mailing_address="", emails=[], phones=[]):

        test_contact = self.find_contact(firstname, lastname)
        if not test_contact:
            new_contact = Contact(
                firstname, lastname,
                mailing_address, emails, phones)

            self.append_contact(new_contact)
        else:
            pass

    def get_nb_contacts(self):
        """ Get the number of contact in the address book. """
        return len(self.book)

    def export_data(self):
        """ Export data as a list of lists. """
        data = []
        for contact in self.book:
            data.append(contact.export_data())

        return data

    def remove_contact(self, sesion, firstname, lastname,):
        contact = self.find_contact(firstname, lastname)
        if contact:
            sesion.delete(contact)

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
        return "<AddressBook {} have {} contact>".format(
            self.name, len(self.contacts))


# -----------------------------------------------------------------------------
#
# ModelManager class
#
# -----------------------------------------------------------------------------
class ModelManager:

    """ This manager will load and save data from a CSV file to build/store
    the list of contacts contained into the address book. """

    DATA_DIR = os.path.join(exe_dir, 'data')
    DATA_FILE = os.path.join(DATA_DIR, 'tact.db')

    def __init__(self):
        """ At all first lauch of the model manager a engine are create """

        if not os.path.exists(ModelManager.DATA_DIR):
            os.mkdir(ModelManager.DATA_DIR)

        ModelManager.engine = create_engine(
            'sqlite:///{}'.format(ModelManager.DATA_FILE), echo=False)
        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=ModelManager.engine)
        self.sesion = Session()

    def close_sesion(self):
        self.sesion.commit()
        self.sesion.close()

    def find_addressbook(self, adressbookname):
        """ Query to find a address email. """

        book = None

        query_find = self.sesion.query(AddressBook).filter(
            AddressBook.name == adressbookname)

        if query_find.all():
            book = query_find.one()

        return book

    def add_contact(
            self, abname, firstname, lastname,
            mailing_address, emails, phones):

        address_book = self.find_addressbook(abname)
        if address_book:
            address_book.add_contact(
                firstname, lastname, mailing_address, emails, phones)

        else:
            address_book = AddressBook(abname)
            address_book.add_contact(
                firstname, lastname, mailing_address, emails, phones)

        print(address_book)

        self.sesion.add(address_book)

        self.close_sesion()

    def find(self, sesion, abname, firstname, lastname):

        contact = None

        address_book = self.find_addressbook(abname)

        if address_book:
            contact = address_book.find_contact(firstname, lastname)

        print(contact)

        self.close_sesion()

    def remove(self, abname, firstname, lastname):

        address_book = self.find_addressbook(abname)

        if address_book:
            address_book.remove_contact(self.sesion, firstname, lastname)

        self.close_sesion()

    def add_phone(self, abname, firstname, lastname, phone):

        address_book = self.find_addressbook(abname)

        if address_book:
            contact = address_book.find_contact(firstname, lastname)
            if contact:
                contact.add_phone(phone)

        self.close_sesion()

    def remove_phone(self, abname, firstname, lastname, phone):

        address_book = self.find_addressbook(abname)

        if address_book:
            contact = address_book.find_contact(firstname, lastname)
            if contact:
                test_phone = contact.find_phone(phone)
                if test_phone:
                    self.sesion.delete(test_phone)
        self.close_sesion()

    def add_email(self, abname, firstname, lastname, email):

        address_book = self.find_addressbook(abname)

        if address_book:
            contact = address_book.find_contact(firstname, lastname)
            if contact:
                contact.add_email(email)
        self.close_sesion()

    def remove_email(self, abname, firstname, lastname, email):

        address_book = self.find_addressbook(abname)

        if address_book:
            contact = address_book.find_contact(firstname, lastname)
            if contact:
                test_email = contact.find_email(email)
                if test_email:
                    self.sesion.delete(test_email)
        self.close_sesion()


# -----------------------------------------------------------------------------
#
# Contact class
#
# -----------------------------------------------------------------------------
class Contact(Base):

    """ Create a new contact (firstname and lastname are obligatory and in
        that order). """

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    mailing_address = Column(String(50), nullable=True)
    phones = relationship("Phone", cascade="all,delete", order_by="Phone.id")
    emails = relationship("Email", cascade="all,delete", order_by="Email.id")
    address_book_id = Column(Integer, ForeignKey('addressbook.id'))

    def __init__(
            self,
            firstname,
            lastname, mailing_address="", emails=[], phones=[]):
        """ Initialisation """

        self.firstname = firstname
        self.lastname = lastname
        self.mailing_address = mailing_address
        for phone in phones:
            if ContactChecker.check_phone(phone):
                correct_phone = Phone(phone)
                self.phones.append(correct_phone)
        for email in emails:
            if ContactChecker.check_email(email):
                correct_email = Email(email)
                self.emails.append(correct_email)

    def export_data(self):  # for saving into a csv or text file
        """ Export data as a list. """
        return [
            self.firstname,
            self.lastname,
            self.mailing_address,
            "|".join(self.emails),
            "|".join(self.phones)
        ]

    def find_phone(self, phonetest):
        """ Find a phone in Contact (if the phone exist already exist) """
        search_phone = None
        tmp_phone = Phone(phonetest)

        for phone in self.phones:
            if phone == tmp_phone:
                search_phone = phone
                LOG.warn(
                    "This phone number {} is (already) atribute to this contact.".format(phone))
                break
        return search_phone

    def add_phone(self, new_phone):
        """ Add the new_phone number in the list of phones of the contact. """

        test_phone = self.find_phone(new_phone)
        if new_phone and \
            ContactChecker.check_phone(new_phone) and \
                not test_phone:
            new_correct_phone = Phone(new_phone)
            self.phones.append(new_correct_phone)

    def remove_phone(self, old_phone):
        """ remove the old_phone number in the list of phones of the contact.
        if this number exist """
        phonetoremove = self.find_phone(old_phone)
        if phonetoremove:
            self.phones.remove(old_phone)

    def find_email(self, emailtest):
        """ Find a contact in AddressBook (if the contact exist) """
        search_email = None
        tmp_email = Email(emailtest)

        for email in self.emails:
            if email == tmp_email:
                search_email = email
                LOG.warn(
                    "This email address {} is (already) atribute to this contact.".format(email))
                break
        return search_email

    def add_email(self, new_email):
        """ Add the new_email in the list of emails of the contact. """
        test_email = self.find_email(new_email)
        if new_email and \
            ContactChecker.check_email(new_email) and \
                not test_email:
            new_correct_email = Email(new_email)
            self.emails.append(new_correct_email)

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
# ContactFactory class for importation of contact
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
# Phone class
#
# -----------------------------------------------------------------------------
class Phone(Base):
    phonenumber = Column(String(22), nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))

    def __init__(self, phone):
        self.phonenumber = phone

    def __eq__(self, other):
        return (
            self.phonenumber == other.phonenumber)

    def __str__(self):
        to_display = "{}".format(self.phonenumber)
        return(to_display)


# -----------------------------------------------------------------------------
#
# Email class
#
# -----------------------------------------------------------------------------
class Email(Base):
    address = Column(String(150), nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))

    def __init__(self, email):
        self.address = email

    def __eq__(self, other):
        return (
            self.address == other.address)

    def __str__(self):
        to_display = "{}".format(self.address)
        return(to_display)


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
