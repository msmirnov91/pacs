import peewee
import os


DB_FILE_NAME = 'loaded_data.db'
db_path = os.path.join(os.getcwd(), 'Storage', DB_FILE_NAME)
db = peewee.SqliteDatabase(db_path)


class LoadedData(peewee.Model):
    path = peewee.CharField(default='')
    name = peewee.CharField(unique=True, null=False)
    comment = peewee.CharField(default='')
    alg = peewee.CharField(default='')
    alg_param = peewee.CharField(default='')

    class Meta:
        database = db


if __name__ == "__main__":
    try:
        LoadedData.create_table()
    except peewee.OperationalError as err:
        print(err)
