import os
import sys
import time

from IO import *
from IO.models import create_db_table
from Recorder.recorder import Recorder


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
except ImportError as error:
    print(error)
    print("Install needed module and try again")
    exit()

create_db_table()

print_success_report()

