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
from tact.core import ModelManager


# Gets execution directory
exe_dir = util.get_exe_dir()

# Sets environment variable for the application
os.environ['TACT_HOME'] = exe_dir
DATA_DIR = os.path.join(exe_dir, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'tact.bd')

# Gets a logger
LOG = util.init_logging()


def execute_add(args):
    """ Executes ADD action with arguments given to the command line. """
    modelmanager = ModelManager()
    modelmanager.add_contact(
        args.addressbook, args.firstname, args.lastname,
        args.mailing_address, args.emails, args.phones)


def execute_find(args):
    modelmanager = ModelManager()
    modelmanager.find(
        args.addressbook, args.firstname, args.lastname)


def execute_remove(args):
    modelmanager = ModelManager()
    modelmanager.remove(
        args.addressbook, args.firstname, args.lastname)


def execute_add_phone(args):
    """ If the contact exist add the phone number given. """
    modelmanager = ModelManager()
    modelmanager.add_phone(
        args.addressbook, args.firstname, args.lastname, args.phone)


def execute_remove_phone(args):
    """ If the contact exist renove the phone number given
    if this last exist. """
    modelmanager = ModelManager()
    modelmanager.remove_phone(
        args.addressbook, args.firstname, args.lastname, args.phone)


def execute_add_email(args):
    """ If the contact exist add the email address given. """
    modelmanager = ModelManager()
    modelmanager.add_email(
        args.addressbook, args.firstname, args.lastname, args.email)


def execute_remove_email(args):
    """ If the contact exist renove the email address given
    if this last exist. """
    modelmanager = ModelManager()
    modelmanager.remove_email(
        args.addressbook, args.firstname, args.lastname, args.email)


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
        'addressbook', action='store', metavar='ADDRESS_BOOK',
        help='a Address Book where the contact must be saved.')

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
        'addressbook', action='store', metavar='ADDRESS_BOOK',
        help='THE Address Book where the contact must be delete.')

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
        'addressbook', action='store', metavar='ADDRESS_BOOK',
        help='THE Address Book where the contact must be modified.')

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
        'addressbook', action='store', metavar='ADDRESS_BOOK',
        help='THE Address Book where the contact must be modified.')

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
        'addressbook', action='store', metavar='ADDRESS_BOOK',
        help='THE Address Book where the contact must be modified.')

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
        'addressbook', action='store', metavar='ADDRESS_BOOK',
        help='THE Address Book where the contact must be modified.')

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
        'addressbook', action='store', metavar='ADDRESS_BOOK',
        help='THE Address Book where the contact must be find.')

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
