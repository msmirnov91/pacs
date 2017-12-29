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

    def get_loaded(self, name):
        db_row = LoadedData.get(LoadedData.name == name)

        data = self.load(db_row.path+self.RESULT_EXT, db_row.name, db_row.comment, has_headers=True)
        data.clustering_alg_name = db_row.alg
        data.clustering_alg_params = db_row.alg_params
        return data

    def store(self, data):
        result_file_name = data.data_name + self.RESULT_EXT
        result_file_dir = os.path.join(self.STORAGE_DIR, self.RESULT_FILES_DIR)
        result_file_path = os.path.join(result_file_dir, result_file_name)
        data.get_data().to_csv(result_file_path)

        new_db_row = LoadedData(path=data.data_name,
                                name=data.data_name,
                                comment=data.user_comment,
                                alg=data.clustering_alg_name,
                                alg_param=data.clustering_alg_params)
        new_db_row.save()

    def load(self, path, name, comment, has_headers=False):
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

        new_data = Data(data, name, comment)
        self.store(new_data)
        return new_data

    def remove(self, name):
        pass

if __name__ == "__main__":
    """
    results = LoadedData.select()
    amount = len(results)

    if amount % 2 == 0:
        new_data = LoadedData(path='test path',
                              name='test{}'.format(amount),
                              comment='test comment',
                              alg='dbscan',
                              alg_param='1')
    else:
        new_data = LoadedData(path='test path',
                              name='test{}'.format(amount),
                              alg_param='1')
    new_data.save()
    """
    results = LoadedData.select()
    for result in results:
        print('path: {} name: {}  comment: {}'.format(result.path, result.name, result.comment))