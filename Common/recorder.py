import logging
import datetime
import os


class Recorder(object):
    REPORTS_DIR = 'Reports'
    __instance = None

    def __init__(self):
        now = datetime.datetime.now()
        self._dir_name = '{}.{}.{}-{}:{}.txt'.format(
            now.day,
            now.month,
            now.year,
            now.hour,
            now.minute
        )

        if not os.path.exists(self.get_record_dir()):
            os.mkdir(self.get_record_dir())

        file_name = 'report.txt'
        file_name = os.path.join(self.get_record_dir(), file_name)
        logging.basicConfig(filename=file_name, level=logging.INFO, format='%(message)s')

    @classmethod
    def add_record(cls, message):
        logging.info(message)

    def get_record_dir(self):
        return os.path.join(self.REPORTS_DIR, self._dir_name)
