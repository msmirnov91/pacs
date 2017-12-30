from Main.gui.tabs.abstract_tab_widget import AbstractTab


class DataInfoTab(AbstractTab):
    def __init__(self, parent=None):
        ui_file = "Info/data_info.ui"
        super(DataInfoTab, self).__init__(ui_file, parent)
        self.name = "Информация"

    def set_data(self, data):
        self.le_name.setText(data.data_name)
        self.le_alg.setText(data.clustering_alg_name)
        self.le_alg_param.setText(data.clustering_alg_params)
        self.le_comment.setText(data.user_comment)
