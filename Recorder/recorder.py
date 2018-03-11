import logging
import datetime
import os


class Recorder(object):
    __instance = None

    def __init__(self, reports_dir):
        self.REPORTS_DIR = reports_dir
        if not os.path.exists(self.get_record_dir()):
            os.makedirs(self.get_record_dir())

        file_name = 'report.txt'
        file_name = os.path.join(self.get_record_dir(), file_name)

        record_msg = ""
        now = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M")

        if not os.path.exists(file_name):
            # lack_of_the_time
            session_name = self.get_record_dir().split('/')[1]
            record_msg = "======SESSION '{}'======\n\n".format(session_name)

        record_msg += "----{}----\n\n".format(str(now))

        logging.basicConfig(filename=file_name, level=logging.INFO, format='%(message)s')
        self.add_record(record_msg)

    @classmethod
    def add_record(cls, message):
        logging.info(message)

    def get_record_dir(self):
        return self.REPORTS_DIR
