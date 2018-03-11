import os

from Main import SESSION_DIR, PACS_DIR
from IO.models import LoadedData, Session
from IO import *
from Common.data import Data


class StorageManager(object):
    def __init__(self, session_name):
        self._session, _ = Session.get_or_create(name=session_name)
        self.result_file_dir = os.path.join(PACS_DIR, SESSION_DIR,
                                            self._session.name, RESULT_FILES_DIR)

        if not os.path.exists(self.result_file_dir):
            os.makedirs(self.result_file_dir)

    def get_all_rows(self):
        return self._session.session_data

    def get_all_names(self):
        rows = self.get_all_rows()
        names = []
        for row in rows:
            names.append(row.name)
        return names

    def get_loaded(self, name):
        db_row = LoadedData.get(name=name, session=self._session)
        data = Data(db_row.name, db_row.comment, db_row.alg, db_row.alg_param)
        data.load_from_file(db_row.path, has_headers=True)
        return data

    def remove_loaded(self, name):
        db_row = LoadedData.get(name=name, session=self._session)
        if os.path.isfile(db_row.path):
            os.remove(db_row.path)
        db_row.delete_instance()

    def store(self, data):
        result_file_name = data.data_name + RESULT_EXT
        result_file_path = os.path.join(self.result_file_dir, result_file_name)
        data.save_to_file(result_file_path)

        new_db_row = LoadedData(name=data.data_name,
                                session=self._session,
                                path=result_file_path,
                                comment=data.user_comment,
                                alg=data.clustering_alg_name,
                                alg_param=data.clustering_alg_params)
        new_db_row.save()

    def load(self, path, name, comment, has_headers=False):
        new_data = Data(name, comment)
        new_data.load_from_file(path, has_headers)
        self.store(new_data)
        return new_data
