import peewee
import os

from IO import *

db_path = os.path.join(os.getcwd(), STORAGE_DIR, DB_FILE_NAME)
db = peewee.SqliteDatabase(db_path)


class LoadedData(peewee.Model):
    path = peewee.CharField(default='')
    name = peewee.CharField(unique=True, null=False)
    comment = peewee.CharField(default='')
    alg = peewee.CharField(default='')
    alg_param = peewee.CharField(default='')

    class Meta:
        database = db


def create_db_table():
    try:
        LoadedData.create_table()
    except peewee.OperationalError as err:
        print(err)
