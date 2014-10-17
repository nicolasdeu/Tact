#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

###
# Project          : Tact
# FileName         : cli.py
# -----------------------------------------------------------------------------
# Author           : Nicolas Deutschmann
# E-Mail           : nicolas.deutschmann@abase.fr
##

import sys
import os
import argparse

from tact import util
from tact.core import Contact
from tact.core import AddressBookManager
import re


def verif(
    a_verif,
    regexp=r"^0[0-9]([ .-]?[0-9]{2}){4}$",
        message=" is not a phone number."):
    if a_verif:
        if re.search(regexp, a_verif) is None:
            print(a_verif, message)
            a_verif = ""
    return (a_verif)


# Gets execution directory
exe_dir = util.get_exe_dir()

# Sets environment variable for the application
os.environ['TACT_HOME'] = exe_dir

# Gets a logger
LOG = util.init_logging()


def execute_add(args):
    """ Executes ADD action with arguments given to the command line. """
    _execute(args, _execute_add)


def _execute_add(args, book, contact):
    if not contact:
        for email in args.emails:
            email = verif(
                email, r"^[A-Za-z1-9]+@[a-z]+[.][a-z]+$", "no correct email")
            if not email:
                args.emails = []
        for phone in args.phones:
            phone = verif(phone)
            if not phone:
                args.phones = []
        new_contact = Contact(
            args.firstname, args.lastname,
            args.mailing_address, args.emails, args.phones)

        book.add_contact(new_contact)

        LOG.info(
            "A new contact has been added in Address Book: {} ".format(
                new_contact))
        LOG.info(
            "There are {} contacts in Address Book."
            .format(book.get_nb_contacts()))


def execute_find(args):
    _execute(args, _execute_find)


def _execute_find(args, book, contact):
    if contact:
        contact.print_contact()


def execute_remove(args):
    _execute(args, _execute_remove)


def _execute_remove(args, book, contact):
    if contact:
        book.remove_contact(contact)


def execute_add_phone(args):
    """ If the contact exist add the phone number given. """
    _execute(args, _execute_add_phone)


def _execute_add_phone(args, book, contact):
    if contact:
        args.phone = verif(args.phone)
        contact.add_phone(args.phone)


def execute_remove_phone(args):
    """ If the contact exist renove the phone number given
    if this last exist. """
    _execute(args, _execute_remove_phone)


def _execute_remove_phone(args, book, contact):
    if contact:
        contact.remove_phone(args.phone)


def execute_add_email(args):
    """ If the contact exist add the email address given. """
    _execute(args, _execute_add_email)


def _execute_add_email(args, book, contact):
    if contact:
        args.email = verif(
            args.email, r"^[A-Za-z1-9]+@[a-z]+[.][a-z]+$", "no correct email")
        contact.add_email(args.email)


def execute_remove_email(args):
    """ If the contact exist renove the email address given
    if this last exist. """
    _execute(args, _execute_remove_email)


def _execute_remove_email(args, book, contact):
    if contact:
        contact.remove_email(args.email)


def _execute(args, task_to_execute):
    book = AddressBookManager.make_address_book()
    contact = book.find_contact(args.firstname, args.lastname)
    task_to_execute(args, book, contact)
    AddressBookManager.save_address_book(book)


def run():
    """ Main command-line execution loop. """
    # Create the arguments parser
    parser = argparse.ArgumentParser(
        description=(
            "Tact is a command-line program for storing contacts into "
            "an address book."
        ),
        prog='tact')

    tact_version = '%(prog)s ' + util.find_version()

    parser.add_argument(
        '--version', action='version',
        version=tact_version)

    # Create Subparsers for each action command
    subparsers = parser.add_subparsers(help='Available actions')

    # ADD action - Arguments parser
    parser_add = subparsers.add_parser(
        'add', help='Add a new Contact in Address Book')

    # Positional arguments for ADD action
    parser_add.add_argument(
        'firstname', action='store', metavar='FIRSTNAME',
        help='Contact firstname.')

    parser_add.add_argument(
        'lastname', action='store', metavar='LASTNAME',
        help='Contact lastname.')

    # Optional arguments for ADD action
    parser_add.add_argument(
        '-m', '--mailing', action='store', metavar="MAILING_ADDRESS",
        help='Contact mailing address (Street, Zip Code, City).',
        dest='mailing_address')

    parser_add.add_argument(
        '-e', '--email', action='append', metavar="EMAIL",
        help='Contact email address', default=[],
        dest='emails')

    parser_add.add_argument(
        '-p', '--phone', action='append', metavar="PHONE",
        help='Contact phone number.', default=[],
        dest='phones')

    # Join ADD subparser with the dedicated execute method
    parser_add.set_defaults(func=execute_add)

    #REMOVE action - Arguments parser
    parser_remove = subparsers.add_parser(
        'remove', help='Add a new Contact in Address Book')

    parser_remove.add_argument(
        'firstname', action='store', metavar='FIRSTNAME',
        help='Contact firstname.')

    parser_remove.add_argument(
        'lastname', action='store', metavar='LASTNAME',
        help='Contact lastname.')

    parser_remove.set_defaults(func=execute_remove)

    # ADD-PHONE action - Arguments parser
    parser_add_phone = subparsers.add_parser(
        'add-phone', help='Add a new phone number to a Contact in Address Book'
        )

    parser_add_phone.add_argument(
        'firstname', action='store', metavar='FIRSTNAME',
        help='Contact firstname.')

    parser_add_phone.add_argument(
        'lastname', action='store', metavar='LASTNAME',
        help='Contact lastname.')

    parser_add_phone.add_argument(
        'phone', action='store', metavar="PHONE",
        help='Contact phone number.')

    parser_add_phone.set_defaults(func=execute_add_phone)

    # REMOVE-PHONE action - Arguments parser
    parser_remove_phone = subparsers.add_parser(
        'remove-phone',
        help='renove a phone number of a Contact in Address Book'
        )

    parser_remove_phone.add_argument(
        'firstname', action='store', metavar='FIRSTNAME',
        help='Contact firstname.')

    parser_remove_phone.add_argument(
        'lastname', action='store', metavar='LASTNAME',
        help='Contact lastname.')

    parser_remove_phone.add_argument(
        'phone', action='store', metavar="PHONE",
        help='Contact phone number.')

    parser_remove_phone.set_defaults(func=execute_remove_phone)

    # ADD-EMAIL action - Arguments parser
    parser_add_email = subparsers.add_parser(
        'add-email', help='Add a new email to a Contact in Address Book'
        )

    parser_add_email.add_argument(
        'firstname', action='store', metavar='FIRSTNAME',
        help='Contact firstname.')

    parser_add_email.add_argument(
        'lastname', action='store', metavar='LASTNAME',
        help='Contact lastname.')

    parser_add_email.add_argument(
        'email', action='store', metavar="EMAIL",
        help='Contact phone number.')

    parser_add_email.set_defaults(func=execute_add_email)

    # REMOVE-EMAIL action - Arguments parser
    parser_remove_email = subparsers.add_parser(
        'remove-email',
        help='renove a emails of a Contact in Address Book'
        )

    parser_remove_email.add_argument(
        'firstname', action='store', metavar='FIRSTNAME',
        help='Contact firstname.')

    parser_remove_email.add_argument(
        'lastname', action='store', metavar='lastname',
        help='Contact lastname.')

    parser_remove_email.add_argument(
        'email', action='store', metavar="EMAIL",
        help='Contact phone number.')

    parser_remove_email.set_defaults(func=execute_remove_email)

    # FIND action - Arguments parser
    parser_find = subparsers.add_parser(
        'find',
        help='find a Contact in Address Book'
        )

    parser_find.add_argument(
        'firstname', action='store', metavar='FIRSTNAME',
        help='Contact firstname.')

    parser_find.add_argument(
        'lastname', action='store', metavar='lastname',
        help='Contact lastname.')

    parser_find.set_defaults(func=execute_find)

    # Parse the arguments line
    try:
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()
    except Exception as error:
        LOG.exception(error)
        sys.exit(2)

    sys.exit()


# EOF
