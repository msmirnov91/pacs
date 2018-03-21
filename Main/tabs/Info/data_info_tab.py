from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab


class DataInfoTab(AbstractVisualizationTab):
    def __init__(self, data, parent=None):
        ui_file = "Info/data_info.ui"
        super(DataInfoTab, self).__init__(ui_file, data=data, parent=parent)
        self.name = "Информация"

    def enable_fields(self):
        self.le_name.setEnabled(True)
        self.le_comment.setEnabled(True)

    def update_tab(self):
        self.le_name.setText(self.data.data_name)
        self.le_alg.setText(self.data.clustering_alg_name)
        self.le_alg_param.setText(self.data.clustering_alg_params)
        self.le_comment.setText(self.data.user_comment)
