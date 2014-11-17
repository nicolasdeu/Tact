#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

###
# Project          : Tact
# FileName         : model.py
# -----------------------------------------------------------------------------
# Author           : Nicolas Deutschmann
# E-Mail           : nicolas.deutschmann@abase.fr
##

import os
import logging
import sqlite3

from tact import util

# Gets execution directory
exe_dir = util.get_exe_dir()

# Logger
LOG = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
#
# DatabaseManager class
#
# -----------------------------------------------------------------------------
class DatabaseManager:

    """ This class will do all operation related to database. """

    # Singleton pattern
    _instance = None

    def __new__(cls, *args, **kwargs):
        """ If there is already a DatabaseManager instance
        returns this one.
        Ensures that there is only one instance of DatabaseManager
        is running in Tact."""
        if not DatabaseManager._instance:
            DatabaseManager._instance = DatabaseManager.__DatabaseManager(
                *args, **kwargs)
        return DatabaseManager._instance

    def __getattr__(self, attr):
        return getattr(self._instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self._instance, attr, val)

    class __DatabaseManager():

        """ Inner class for Singleton purpose. """

        def __init__(self, database_url):
            """ Initializes instance. """
            LOG.debug("Database URL: {}".format(database_url))
            self.db_url = database_url

            if not os.path.exists(database_url):
                self.initialize_db()

        def initialize_db(self):
            LOG.debug("Initializes Database.")

            try:
                # Create new db and make connection
                db_connection = sqlite3.connect(self.db_url)
                db_cursor = db_connection.cursor()

                # Enable Foreign Keys support
                db_cursor.execute("PRAGMA foreign_keys=ON")

                # Create address_book table
                db_cursor.execute(
                    """ CREATE TABLE IF NOT EXISTS address_book
                        (id INTEGER PRIMARY KEY, name TEXT NOT NULL) """)

                # Create contact table
                db_cursor.execute(
                    """ CREATE TABLE IF NOT EXISTS contact (
                        id INTEGER PRIMARY KEY,
                        firstname TEXT NOT NULL,
                        lastname TEXT NOT NULL,
                        home_address TEXT,
                        address_book_id INTEGER,
                        FOREIGN KEY (address_book_id)
                            REFERENCES address_book(id)) """)

                # Create phone table
                db_cursor.execute(
                    """ CREATE TABLE IF NOT EXISTS phone (
                        id INTEGER PRIMARY KEY,
                        number TEXT NOT NULL,
                        contact_id INTEGER,
                        FOREIGN KEY (contact_id) REFERENCES contact(id)) """)

                # Create email table
                db_cursor.execute(
                    """ CREATE TABLE IF NOT EXISTS email (
                        id INTEGER PRIMARY KEY,
                        address TEXT NOT NULL,
                        contact_id INTEGER,
                        FOREIGN KEY (contact_id) REFERENCES contact(id)) """)

                # Save (commit) the changes
                db_connection.commit()

                # Close connection
                db_connection.close()
            except Exception as error:
                LOG.error(
                    "Error during initialization of Database: {}".format(
                        error))

        def load_data(self, address_book):
            LOG.debug("Load data from database.")

            try:
                # Make connection
                db_connection = sqlite3.connect(self.db_url)
                db_cursor = db_connection.cursor()

                # Query address_book table
                db_cursor.execute(
                    """ SELECT
                        address_book.id,
                        contact.id,
                        contact.firstname,
                        contact.lastname,
                        contact.home_address,
                        phone.number,
                        email.address
                        FROM address_book, contact
                        LEFT JOIN phone ON contact.id = phone.contact_id
                        LEFT JOIN email ON contact.id = email.contact_id
                        WHERE address_book.id = contact.address_book_id
                        AND address_book.name = ? """,
                    (address_book.name, ))

                for data in db_cursor:
                    address_book_id = data[0]
                    contact_id = data[1]
                    firstname = data[2]
                    lastname = data[3]
                    home_address = data[4]
                    phone = data[5]
                    email = data[6]

                    address_book.id = address_book_id

                    # If contact has multiple phone numbers
                    # it will appear multiple times.
                    # Thus search him first
                    # before adding him again in address book.
                    cur_contact = address_book.find_contact(
                        firstname, lastname)

                    if not cur_contact:
                        cur_contact = address_book.add_contact(
                            firstname, lastname, home_address)

                    cur_contact.id = contact_id

                    cur_contact.add_phone(phone)
                    cur_contact.add_email(email)

                # Close connection
                db_connection.close()
            except Exception as error:
                LOG.error(
                    "Error during data loading: {}".format(
                        error))

        def save_data(self, address_book):
            LOG.debug("Save data to database.")

            try:
                # Make connection
                db_connection = sqlite3.connect(self.db_url)
                db_cursor = db_connection.cursor()

                # Insert or update the address book
                if hasattr(address_book, "id"):
                    db_cursor.execute(
                        """ UPDATE address_book SET name = ? WHERE id = ? """,
                        (address_book.name, address_book.id))
                else:
                    db_cursor.execute(
                        """ INSERT INTO address_book (name)
                            VALUES (?)""", (address_book.name, ))
                    address_book.id = db_cursor.lastrowid

                # Insert or update all contact from address book
                for contact in address_book.book:
                    if hasattr(contact, "id"):
                        db_cursor.execute(
                            """ UPDATE contact
                                SET
                                    firstname = ?,
                                    lastname = ?,
                                    home_address = ?
                                WHERE id = ? AND address_book_id = ? """, (
                                contact.firstname,
                                contact.lastname,
                                contact.mailing_address,
                                contact.id, address_book.id))
                    else:
                        db_cursor.execute(
                            """ INSERT INTO contact (
                                    firstname,
                                    lastname,
                                    home_address,
                                    address_book_id)
                                VALUES (?, ?, ?, ?) """, (
                                contact.firstname,
                                contact.lastname,
                                contact.mailing_address,
                                address_book.id))
                        contact.id = db_cursor.lastrowid

                    # Clean phone table for current contact
                    db_cursor.execute(
                        """ DELETE FROM phone
                            WHERE contact_id = ? """, (contact.id, ))

                    # Clean email table for current contact
                    db_cursor.execute(
                        """ DELETE FROM email
                            WHERE contact_id = ? """, (contact.id, ))

                    # Insert all phone numbers
                    for phone in contact.phones:
                        db_cursor.execute(
                            """ INSERT INTO phone (number, contact_id)
                                VALUES (?, ?) """, (phone, contact.id))

                    # Insert all email addresses
                    for email in contact.emails:
                        db_cursor.execute(
                            """ INSERT INTO email (address, contact_id)
                                VALUES (?, ?) """, (email, contact.id))

                # Save (commit) the changes
                db_connection.commit()

                # Close connection
                db_connection.close()
            except Exception as error:
                LOG.error(
                    "Error during data saving: {}".format(
                        error))


# EOF
