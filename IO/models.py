import peewee
import os

from IO import *

db_path = os.path.join(os.getcwd(), DB_FILE_NAME)
db = peewee.SqliteDatabase(db_path)


# one-to-many
class Session(peewee.Model):
    id = peewee.PrimaryKeyField(null=False)
    name = peewee.CharField(unique=True, null=False)
    plot_amount = peewee.IntegerField(default=0)
    bww_amount = peewee.IntegerField(default=0)
    bar_amount = peewee.IntegerField(default=0)
    matrix_amount = peewee.IntegerField(default=0)
    vector_amount = peewee.IntegerField(default=0)
    pie_amount = peewee.IntegerField(default=0)

    class Meta:
        database = db


class LoadedData(peewee.Model):
    id = peewee.PrimaryKeyField(null=False)
    name = peewee.CharField(null=False)
    session = peewee.ForeignKeyField(Session, related_name='session_data')
    path = peewee.CharField(default='')
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

    try:
        Session.create_table()
    except peewee.OperationalError as err:
        print(err)
