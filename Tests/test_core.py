#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

###
# Project          : Tact
# FileName         : test_core.py
# -----------------------------------------------------------------------------
# Author           : Nicolas Deutschmann
# E-Mail           : nicolas.deutschmann@abase.fr
##

import unittest

from tact.core import AddressBook
from tact.core import Contact


# -----------------------------------------------------------------------------
#
# ContactTestCase class
#
# -----------------------------------------------------------------------------
class ContactTestCase(unittest.TestCase):
    """ Test Contact class. """

    def test_init_contact(self):
        """ Test initialization of a new Contact object. """
        expected_firstname_01 = "Albert"
        expected_lastname_01 = "Einstein"

        # Create a new Contact
        contact_01 = Contact(expected_firstname_01, expected_lastname_01)

        # Assert that firstname and lastname have been correctly assigned
        self.assertEqual(contact_01.firstname, expected_firstname_01)
        self.assertEqual(contact_01.lastname, expected_lastname_01)


# -----------------------------------------------------------------------------
#
# AddressBookTestCase class
#
# -----------------------------------------------------------------------------
class AddressBookTestCase(unittest.TestCase):
    """ Test Address Book class. """

    def test_add_contact(self):
        """ Test adding a new contact in address book. """
        # Create a new address book and a contact
        address_book = AddressBook()
        contact = Contact("Brigitte", "Alphonse")

        address_book.add_contact(contact)

        self.assertEqual(address_book.get_nb_contacts, 1)


if __name__ == "__main__":
    unittest.main()

# EOF
