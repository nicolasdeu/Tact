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
from tact.core import AddressBook
from tact.IO import CSVManager

# Gets execution directory
exe_dir = util.get_exe_dir()

# Sets environment variable for the application
os.environ['TACT_HOME'] = exe_dir

# Gets a logger
LOG = util.init_logging()


def execute_add(args):
    """ Executes ADD action with arguments given to the command line. """
    csv_manager = CSVManager()
    data = csv_manager.load()

    new_contact = Contact(
        args.firstname, args.lastname,
        args.mailing_address, args.emails, args.phones)

    an_address_book = AddressBook()
    an_address_book.import_data(data)
    an_address_book.add_contact(new_contact)

    LOG.info(
        "A new contact has been added in Address Book: {} ".format(
            new_contact))
    LOG.info(
        "There are {} contacts in Address Book."
        .format(an_address_book.get_nb_contacts()))

    data = an_address_book.export_data()
    csv_manager.save(data)


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
        '-e', '--email', action='store', metavar="EMAIL",
        help='Contact email address',
        dest='email')

    parser_add.add_argument(
        '-p', '--phone', action='store', metavar="PHONE",
        help='Contact phone number.',
        dest='phone')

    # Join ADD subparser with the dedicated execute method
    parser_add.set_defaults(func=execute_add)

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
