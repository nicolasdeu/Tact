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
from sqlalchemy.orm import sessionmaker, relationship, backref

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
        "Contact", order_by="Contact.id", backref="addressbook")

    def __init__(self, name="default"):
        self.name = name

    def append_contact(self, contact):
        """ Add a contact directly into AddressBook without any check. """
        self.contacts.append(contact)

    def add_contact(
            self,
            firstname, lastname,
            mailing_address="", emails=[], phones=[]):
        new_contact = Contact(
            firstname, lastname,
            mailing_address, emails, phones)

        self.append_contact(new_contact)

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
        return "<AddressBook {} >" .format(self.id)


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

    def find_phone(self, sesion, contactid, phone):
        """ query to find a contact phone """

        search_phone = None

        query_find = sesion.query(Phone).filter(
            Phone.contact_id == contactid).filter(
            Phone.phonenumber == phone)
        if query_find.all():
            search_phone = query_find.one()

        return search_phone

    def find_email(self, sesion, contactid, email):
        """ query to find a contact email """

        search_email = None

        query_find = sesion.query(Email).filter(
            Email.contact_id == contactid).filter(
            Email.address == email)
        if query_find.all():
            search_email = query_find.one()

        return search_email

    def find_contact(self, sesion, addressbookid, firstname, lastname):
        """ query to find a contact """

        search_contact = None

        query_find = sesion.query(Contact).filter(
            Contact.address_book_id == addressbookid).filter(
            Contact.firstname == firstname).filter(
            Contact.lastname == lastname)
        if query_find.all():
            search_contact = query_find.one()

        return search_contact

    def find_id_contact(self, sesion, addressbookid, firstname, lastname):
        """ Query to find a contact id. """

        idcontact = None

        query_find = sesion.query(Contact.id).filter(
            Contact.address_book_id == addressbookid).filter(
            Contact.firstname == firstname).filter(
            Contact.lastname == lastname)
        #print(query_find)
        if query_find.all():
            idcontact = query_find.one()
            idcontact = idcontact[0]

        #sesion.close()

        return idcontact

    def find_addressbook(self, sesion, adressbookname):
        """ Query to find a address email. """

        book = None

        query_find = sesion.query(AddressBook).filter(
            AddressBook.name == adressbookname)
        #print(query_find)
        if query_find.all():
            book = query_find.one()

        print(book)

        #sesion.close()

        return book

    def find_id_addressbook(self, sesion, adressbookname):

        idab = None

        query_find = sesion.query(AddressBook.id).filter(
            AddressBook.name == adressbookname)
        #print(query_find)
        if query_find.all():
            idab = query_find.one()
            idab = idab[0]

        print(type(idab))

        #sesion.close()

        return idab

    def add_contact(
            self, abname, firstname, lastname,
            mailing_address, emails, phones):

        Session = sessionmaker(bind=ModelManager.engine)
        sesion = Session()

        address_book = self.find_addressbook(sesion, abname)
        if address_book:
            print(address_book)
            abid = self.find_id_addressbook(sesion, abname)
            test_contact = self.find_contact(
                sesion, abid, firstname, lastname)
            if test_contact:
                print(test_contact)
            else:
                address_book.add_contact(
                    firstname, lastname, mailing_address, emails, phones)

            #print("test")
        else:
            address_book = AddressBook(abname)
            address_book.add_contact(
                firstname, lastname, mailing_address, emails, phones)

        #print("test")

        sesion.add(address_book)
        sesion.commit()

        sesion.close()

    def find(
            self, abname, firstname, lastname):

        Session = sessionmaker(bind=ModelManager.engine)
        sesion = Session()
        contact = None

        id_address_book = self.find_id_addressbook(sesion, abname)

        if id_address_book:
            contact = self.find_contact(
                sesion, id_address_book, firstname, lastname)

        print(contact)

        sesion.close()

    def remove(self, abname, firstname, lastname):

        Session = sessionmaker(bind=ModelManager.engine)
        sesion = Session()

        id_address_book = self.find_id_addressbook(sesion, abname)

        if id_address_book:
            contact = self.find_contact(
                sesion, id_address_book, firstname, lastname)
            sesion.delete(contact)

        sesion.commit()

        sesion.close()

    def add_phone(self, abname, firstname, lastname, phone):
        Session = sessionmaker(bind=ModelManager.engine)
        sesion = Session()

        print("test")

        id_address_book = self.find_id_addressbook(sesion, abname)

        print("test")

        if id_address_book:
            contact = self.find_contact(
                sesion, id_address_book, firstname, lastname)
            if contact:
                id_contact = self.find_id_contact(
                    sesion, id_address_book, firstname, lastname)
                test_phone = self.find_phone(sesion, id_contact, phone)
                if not test_phone:
                    contact.add_phone(phone)

        sesion.commit()

        sesion.close()

    def remove_phone(self, abname, firstname, lastname, phone):
        Session = sessionmaker(bind=ModelManager.engine)
        sesion = Session()

        print("test")

        id_address_book = self.find_id_addressbook(sesion, abname)

        print("test")

        if id_address_book:
            contact = self.find_contact(
                sesion, id_address_book, firstname, lastname)
            if contact:
                id_contact = self.find_id_contact(
                    sesion, id_address_book, firstname, lastname)
                test_phone = self.find_phone(sesion, id_contact, phone)
                if test_phone:
                    sesion.delete(test_phone)

        sesion.commit()

        sesion.close()

    def add_email(self, abname, firstname, lastname, email):
        Session = sessionmaker(bind=ModelManager.engine)
        sesion = Session()

        print("test")

        id_address_book = self.find_id_addressbook(sesion, abname)

        print("test")

        if id_address_book:
            contact = self.find_contact(
                sesion, id_address_book, firstname, lastname)
            if contact:
                id_contact = self.find_id_contact(
                    sesion, id_address_book, firstname, lastname)
                test_email = self.find_email(sesion, id_contact, email)
                if not test_email:
                    contact.add_email(email)

        sesion.commit()

        sesion.close()

    def remove_email(self, abname, firstname, lastname, email):
        Session = sessionmaker(bind=ModelManager.engine)
        sesion = Session()

        print("test")

        id_address_book = self.find_id_addressbook(sesion, abname)

        print("test")

        if id_address_book:
            contact = self.find_contact(
                sesion, id_address_book, firstname, lastname)
            if contact:
                id_contact = self.find_id_contact(
                    sesion, id_address_book, firstname, lastname)
                test_email = self.find_email(sesion, id_contact, email)
                if test_email:
                    sesion.delete(test_email)

        sesion.commit()

        sesion.close()


#        """ Save ddress book on disk into a DB file. """
#        Session = sessionmaker(bind=ModelManager.engine)
#        sesion = Session()
#        for elem in address_book.book:
#            sesion.add(elem)
#        sesion.commit()
#        sesion.close()


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
    phones = relationship("Phone", order_by="Phone.id")
    emails = relationship("Email", order_by="Email.id")
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

    def add_phone(self, new_phone):
        """ Add the new_phone number in the list of phones of the contact. """
        if new_phone and \
            ContactChecker.check_phone(new_phone) and \
                new_phone not in self.phones:
            new_correct_phone = Phone(new_phone)
            self.phones.append(new_correct_phone)
        el

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
