import re

from sklearn.decomposition import PCA
from sklearn import preprocessing

from PyQt4.QtGui import QStandardItemModel, QStandardItem, QAbstractItemView

from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
from Main.tabs.adviser_tab_mixin import AdviserTabMixin
from Main import PACS_DIR
from Main.Plot.coords_plot_widget import CoordsPlot

from Recorder.recorder import Recorder


class PreprocessingTab(AbstractVisualizationTab, AdviserTabMixin):
    def __init__(self, data, parent=None):
        ui_file = PACS_DIR + "/Main/tabs/Preprocessing/preprocessing.ui"
        super(PreprocessingTab, self).__init__(ui_file, data=data, parent=parent)
        self.name = "Предварительая обработка"

        self.plot = CoordsPlot()
        self.scatter_plot_layout.addWidget(self.plot)

        # lack_of_the_time
        self.element_numbers = []
        self.lv_coordinates.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.cb_use_all.toggled.connect(self._enable_choose_data)
        self.pb_select.clicked.connect(self.reduce_data)

        self.pca_pb.clicked.connect(self.do_pca)
        self.normalize_pb.clicked.connect(self.normalize)

    def update_tab(self):
        data_has_names = self.data.has_names()
        self.le_element_numbers.setEnabled(data_has_names)  # disable if data hsd no names
        if data_has_names:
            self.element_numbers = self.data.get_element_names()

        model = QStandardItemModel(self.lv_coordinates)
        for coord in self.data.get_coords_list():
            item = QStandardItem(str(coord))
            model.appendRow(item)
        self.lv_coordinates.setModel(model)

        self.plot.update_tab(self.data)

        data_coords_amount = len(self.data.get_coords_list())
        self.pc_amount.setRange(0, data_coords_amount)
        self.pc_amount.setValue(0)

    def _enable_choose_data(self):
        if self.cb_use_all.isChecked():
            self.gb_choose_data.setEnabled(False)
        else:
            self.gb_choose_data.setEnabled(True)

    def use_all_data(self):
        return self.cb_use_all.isChecked()

    def get_choosed_coords(self):
        coords_list = []
        for index in self.lv_coordinates.selectedIndexes():
            coords_list.append(str(index.data()))
        return coords_list

    def reduce_data(self):
        coords = self.get_choosed_coords()
        if coords:
            self.data.select_coordinates(coords)

        elements_descriptions = self.le_element_numbers.text()
        if elements_descriptions:
            elements = []

            elements_descriptions = elements_descriptions.replace(" ", "")
            elements_descriptions = elements_descriptions.split(",")
            range_regexp = '\d\-\d'
            digit_regexp = '\d'

            for description in elements_descriptions:
                if re.match(range_regexp, description):
                    description = description.split("-")
                    first_element = int(description[0])
                    last_element = int(description[1])
                    for i in range(first_element, last_element+1):
                        elements.append(i)
                elif re.match(digit_regexp, description):
                    elements.append(int(description))

            elements = list(set(elements))  # leave only unique elements
            self.data.select_elements(elements)

    def do_pca(self):
        components_amount = self.pc_amount.value()
        pca = PCA(n_components=components_amount)
        df = self.data.get_dataframe()
        pca.fit(df)
        self.data.set_dataframe(pca.transform(df))
        self.update_tab()

        record_msg = "PCA.\n\tdata: {}\n\tn_components:{}\n".format(self.data.data_name,
                                                                    components_amount)
        Recorder.get_instance().add_record(record_msg)

    def normalize(self):
        x = self.data.get_dataframe()
        new_df = preprocessing.MaxAbsScaler().fit_transform(x)
        self.data.set_dataframe(new_df)
        self.update_tab()

        record_msg = "Scaling.\n\tdata: {}\n".format(self.data.data_name)
        Recorder.get_instance().add_record(record_msg)

    # lack_of_the_time
    def get_description_for_report(self):
        return self.plot.get_description_for_report()

    # lack_of_the_time
    def add_image_to_report(self, rep_dir, number):
        return self.plot.add_image_to_report(rep_dir, number)

    # lack_of_the_time
    def get_plot_name(self):
        return self.plot.get_plot_name()

