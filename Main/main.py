import copy
import re

from PyQt4 import uic
from PyQt4.QtGui import *

from Generator.generator_dialog import GeneratorDialog
from IO.gui.load_widget import LoadWidget
from IO.gui.save_widget import SaveWidget
from IO.storage_manager import StorageManager
from Main.tabs.Adviser.adviser_tab import AdviserTab
from Main.tabs.Clustering.clustering_tab import ClusteringTab
from Main.tabs.Comparison.comparison_tab import ComparisonTab
from Main.tabs.Info.data_info_tab import DataInfoTab
from Main.tabs.Plot.plot_tab import PlotTab
from Main.tabs.Representation.representation_tab import RepresentationTab
from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
from Processor.processor import Processor
from Recorder.recorder import Recorder


class PACS(QMainWindow):
    def __init__(self, parent=None):
        super(PACS, self).__init__(parent)
        uic.loadUi("Main/main.ui", self)
        self.setWindowIcon(QIcon("Main/icon.gif"))

        self._recorder = Recorder()

        self.tabs = [
            DataInfoTab(),
            PlotTab(),
            ClusteringTab(),
            ComparisonTab(),
            RepresentationTab(),
            AdviserTab()
        ]

        self.clustering_tab = self.tabs[2]

        for tab in self.tabs:
            self.tab_main.addTab(tab, tab.name)

        self._data_1 = None
        self._data_2 = None

        self.list_data.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.connect_signals_and_slots()
        self.update_data_list()

    def connect_signals_and_slots(self):
        self.btn_select.clicked.connect(self.select_data)
        self.btn_load_new.clicked.connect(self.load_new_data)
        self.btn_generate.clicked.connect(self.generate_data)
        self.btn_save.clicked.connect(self.save_result)
        self.btn_remove.clicked.connect(self.remove_data)
        self.actionSave_image_for_report.triggered.connect(self.save_curr_plot_for_report)

        self.tabs[2].clusterize_data.connect(self.clusterize_data)

    def load_new_data(self):
        load_widget = LoadWidget()
        load_widget.exec_()
        # lack_of_the_time
        self.update_data_list()

    def select_data(self):
        selected_items = self.list_data.selectedIndexes()
        items_amount = len(selected_items)

        if items_amount == 1:
            self._data_1 = StorageManager().get_loaded(selected_items[0].data())
            self._data_2 = None
        elif items_amount == 2:
            self._data_1 = StorageManager().get_loaded(selected_items[0].data())
            self._data_2 = StorageManager().get_loaded(selected_items[1].data())
        else:
            return

        record_msg = "Selected data:\n\t{}\n".format(self._data_1.data_name)
        if self._data_2:
            log_2_data = "\t{}\n".format(self._data_2.data_name)
            record_msg += log_2_data
        self._recorder.add_record(record_msg)

        self.update_tabs()

    def generate_data(self):
        generate_dialog = GeneratorDialog()
        result = generate_dialog.exec_()

        if result:
            record_msg = "Generated data:\n\tname: {}\n\tdescription: {}\n"
            record_msg = record_msg.format(generate_dialog.get_data_name(),
                                           generate_dialog.get_description())
            self._recorder.add_record(record_msg)

        self.update_data_list()

    def save_result(self):
        if self._data_1 is None:
            return

        save_widget = SaveWidget(self._data_1)
        result = save_widget.exec_()

        if result:
            record_msg = "Saved data:\n\t{}\n".format(self._data_1.data_name)
            self._recorder.add_record(record_msg)

        self.update_data_list()

    def remove_data(self):
        storage_manager = StorageManager()
        selected_items = self.list_data.selectedIndexes()
        for item in selected_items:
            storage_manager.remove_loaded(item.data())

        self.update_data_list()

    def clusterize_data(self):
        if self._data_1 is None:
            return

        if not self.clustering_tab.use_all_data():
            self._reduce_data(self.clustering_tab.get_choosed_coords(),
                              self.clustering_tab.get_choosed_names())

        alg, params = self.clustering_tab.get_algorithm_and_settings()
        labels = Processor().get_cluster_labels(self._data_1, alg, params)
        self._data_1.set_labels(labels)
        self._data_1.clustering_alg_name = alg
        self._data_1.clustering_alg_params = str(params)

        # lack_of_the_time
        record_msg = """Clustered data:
        \tdata: {}
        \tcoordinates: {}
        \telements: {}
        \talgorithm: {}
        \tparameters: {}\n"""

        self._recorder.add_record(record_msg.format(self._data_1.data_name,
                                                    self._data_1.get_coords_list(),
                                                    self._data_1.get_elements_names_string(),
                                                    self._data_1.clustering_alg_name,
                                                    self._data_1.clustering_alg_params))
        self.update_tabs()

    def update_data_list(self):
        data_list_model = QStandardItemModel(self.list_data)
        names = StorageManager().get_all_names()
        for name in names:
            item = QStandardItem(name)
            data_list_model.appendRow(item)
        self.list_data.setModel(data_list_model)

    def update_tabs(self):
        for tab in self.tabs:
            if not tab.is_visualization_tab:
                continue

            # to prevent data corrupting
            data_1_copy = copy.deepcopy(self._data_1)

            if tab.need_two_data_sets:
                data_2_copy = copy.deepcopy(self._data_2)
                tab.update_tab(self._data_1, data_2_copy)
            else:
                tab.update_tab(data_1_copy)

    def _reduce_data(self, coords, elements_descriptions):
        if coords:
            self._data_1.select_coordinates(coords)

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
            self._data_1.select_elements(elements)

    def save_curr_plot_for_report(self):
        current_widget_index = self.tab_main.currentIndex()
        current_widget = self.tab_main.widget(current_widget_index)

        if isinstance(current_widget, AbstractVisualizationTab):
            report_dir = self._recorder.get_record_dir()
            img_name = current_widget.add_image_to_report(report_dir)
            report_description = current_widget.get_description_for_report()
            self._recorder.add_record("Was saved {}.\n\tname: {}\n".format(report_description, img_name))

    def main(self):
        self.show()
