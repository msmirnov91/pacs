import peewee


db = peewee.SqliteDatabase("loaded_data.db")


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
    except peewee.OperationalError:
        print("Table already exists!")
