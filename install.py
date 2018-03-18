import sys
import time

from Main import *
from IO.models import create_db_table


def print_slowly(message, delay):
    for letter in message:
        print(letter, end="")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_success_report():
    print("PACS installed successfully!")
    time.sleep(1)
    print_slowly("...at least i hope so.", 0.2)
    time.sleep(1)
    print_slowly("Good luck.", 0.35)


try:
    import PyQt4
    import matplotlib
    import numpy
    import peewee
    import scipy
    import sklearn
except ImportError as error:
    print(error)
    print("Install needed module and try again")
    exit()

create_db_table()
os.makedirs(SESSION_DIR)

print_success_report()

