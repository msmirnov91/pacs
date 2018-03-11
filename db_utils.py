import os
from IO.models import create_db_table, LoadedData, Session, db_path


class DbUtils:
    @classmethod
    def lsdb(cls):
        """
        shows all db instances
        :return:
        """
        sessions = Session.select()
        session_report = "-Session name: '{}'. Saved:\n plt: {}, bww: {}, bar: {}, matrix: {}, vector: {}, pie: {}"
        print("All sessions: ")
        for session in sessions:
            print(session_report.format(session.name,
                                        session.plot_amount,
                                        session.bww_amount,
                                        session.bar_amount,
                                        session.matrix_amount,
                                        session.vector_amount,
                                        session.pie_amount))

        data = LoadedData.select()
        data_rep_template = "-Data name: '{}'. Session name: '{}', file path: {}"
        print("\nAll data:")
        for d in data:
            print(data_rep_template.format(d.name, d.session.name, d.path))

    @classmethod
    def rmdb(cls):
        """
        removes db file
        :return:
        """
        os.remove(db_path)
        print("db was removed")

    @classmethod
    def rm(cls):
        """
        removes single row
        :return:
        """
        print("Data or session must be removed?")

        table_name = input().lower()

        if table_name == "data":
            table = LoadedData
        elif table_name == "session":
            table = Session
        else:
            print("unknown table")
            return

    @classmethod
    def mrproper(cls):
        """
        clears all db tables
        :return:
        """
        q1 = Session.delete()
        q2 = LoadedData.delete()
        q1.execute()
        q2.execute()
        print("db was cleared")

    @classmethod
    def mkdb(cls):
        """
        makes db file and creates needed tables
        :return:
        """
        create_db_table()
        print("db file and tables created")

    @classmethod
    def help(cls):
        print("====================")
        print("lsdb - shows all db instances")
        print("rmdb - removes db file")
        print("mrproper - clears all db tables")
        print("mkdb - makes db file and creates needed tables")
        print("rm - removes single row")
        print("q - quit")
        print("====================")

if __name__ == "__main__":
    print("Database CLI. Type command or 'help'")
    while True:
        cmd = input()
        if cmd == "q":
            break

        if hasattr(DbUtils, cmd):
            getattr(DbUtils, cmd)()
        else:
            print("wrong command")
