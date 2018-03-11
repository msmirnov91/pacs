from IO.models import create_db_table, LoadedData, Session


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
        pass

    @classmethod
    def mrproper(cls):
        """
        clears all db tables
        :return:
        """
        pass

    @classmethod
    def mkdb(cls):
        """
        makes db file and creates needed tables
        :return:
        """
        create_db_table()
        print("db file and tables created")


if __name__ == "__main__":
    print("DB CLI. Type command")
    print("====================")
    print("lsdb - shows all db instances")
    print("rmdb - removes db file")
    print("mrproper - clears all db tables")
    print("mkdb - makes db file and creates needed tables")
    print("q - quit")
    print("====================")
    while True:
        cmd = input()
        if cmd == "q":
            break

        if hasattr(DbUtils, cmd):
            getattr(DbUtils, cmd)()
        else:
            print("wrong command")
