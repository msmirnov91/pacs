import os
import sys

from Common.recorder import Recorder
from IO import *
from IO.models import create_db_table

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

storage_dir = os.path.join(os.getcwd(), STORAGE_DIR)

os.mkdir(storage_dir)
os.mkdir(Recorder.REPORTS_DIR)

data_dirs = [RAW_FILES_DIR, RESULT_FILES_DIR]

for data_dir in data_dirs:
    os.mkdir(os.path.join(storage_dir, data_dir))

create_db_table()
