import os

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
        data = Data(db_row.name, db_row.comment, db_row.alg, db_row.alg_param)
        data.load_from_file(db_row.path, has_headers=True)
        return data

    def store(self, data):
        result_file_name = data.data_name + self.RESULT_EXT
        result_file_dir = os.path.join(self.STORAGE_DIR, self.RESULT_FILES_DIR)
        result_file_path = os.path.join(result_file_dir, result_file_name)
        data.save_to_file(result_file_path)

        new_db_row = LoadedData(path=result_file_path,
                                name=data.data_name,
                                comment=data.user_comment,
                                alg=data.clustering_alg_name,
                                alg_param=data.clustering_alg_params)
        new_db_row.save()

    def load(self, path, name, comment, has_headers=False):
        new_data = Data(name, comment)
        new_data.load_from_file(path, has_headers)
        self.store(new_data)
        return new_data

    def remove(self, name):
        pass

if __name__ == "__main__":
    rows = StorageManager().get_all_rows()
    for row in rows:
        print('path: {} name: {}  comment: {}'.format(row.path, row.name, row.comment))
