import os

import peewee
import pandas as pd

from IO.models import LoadedData
from Common.data import Data


class StorageManager(object):
    STORAGE_DIR = 'Storage'
    RAW_FILES_DIR = 'Raw'
    RESULT_FILES_DIR = 'Files'
    RESULT_EXT = '.clust'

    @classmethod
    def get_all_rows(cls):
        return LoadedData.select()

    def get_all_names(self):
        rows = self.get_all_rows()
        names = []
        for row in rows:
            names.append(row.name)
        return names

    def get_loaded(self, name):
        db_row = LoadedData.get(LoadedData.name == name)
        csv_data = self._load_csv(db_row.path, has_headers=True)
        return Data(csv_data, db_row.name, db_row.comment, db_row.alg, db_row.alg_param)

    def store(self, data):
        result_file_name = data.data_name + self.RESULT_EXT
        result_file_dir = os.path.join(self.STORAGE_DIR, self.RESULT_FILES_DIR)
        result_file_path = os.path.join(result_file_dir, result_file_name)
        data.get_data().to_csv(result_file_path)

        new_db_row = LoadedData(path=result_file_path,
                                name=data.data_name,
                                comment=data.user_comment,
                                alg=data.clustering_alg_name,
                                alg_param=data.clustering_alg_params)
        new_db_row.save()

    def load(self, path, name, comment, has_headers=False):
        data = self._load_csv(path, has_headers)
        new_data = Data(data, name, comment)
        self.store(new_data)
        return new_data

    @classmethod
    def _load_csv(cls, path, has_headers=False):
        if path is None or path == "":
            return

        if has_headers:
            data = pd.read_csv(path)
        else:
            data = pd.read_csv(path, header=None)
            column_names = []
            for i in range(0, len(data.columns)):
                column_names.append("x{}".format(i))
            data.columns = column_names

        return data

    def remove(self, name):
        pass

if __name__ == "__main__":
    rows = StorageManager().get_all_rows()
    for row in rows:
        print('path: {} name: {}  comment: {}'.format(row.path, row.name, row.comment))
