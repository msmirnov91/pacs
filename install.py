import os

from IO.storage_manager import StorageManager
from IO.models import create_db_table

storage_dir = os.path.join(os.getcwd(), StorageManager.STORAGE_DIR)
os.mkdir(storage_dir)

data_dirs = [StorageManager.RAW_FILES_DIR, StorageManager.RESULT_FILES_DIR]

for data_dir in data_dirs:
    os.mkdir(os.path.join(storage_dir, data_dir))

create_db_table()
