import csv
import os

from tact.util import get_exe_dir


exe_dir = get_exe_dir()
tactcsv = os.path.join(exe_dir, 'data', 'tact.csv')


class CSVManager:

    """ manage the tact.csv """

    def __init__(self):
        """ Initialisation:create tact.csv if he not exist """
        if not os.path.exists(tactcsv):
            with open(tactcsv, 'w', newline='') as data:
                writer = csv.writer(data)
                writer.writerow([
                    'Firstname',
                    'Lastname', 'Home Address', 'Emails', 'Phones'])

    def load(self):
        with open(tactcsv, newline='') as data:

            liste_data = []
            reader = csv.reader(data)
            for line in reader:
                liste_data.append(line)

    def save(self, input_data):
        """ Save the data in tact.csv and in one line. """

        with open(tactcsv, 'w', newline='') as data:

            writer = csv.writer(data)

            writer.writerows(input_data)
