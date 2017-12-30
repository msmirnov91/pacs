from PyQt4 import uic
from PyQt4.QtGui import *

from IO.storage_manager import StorageManager

# TODO: put them all in one file!
from IO.gui.load_widget import LoadWidget
from Main.gui.tabs.Info.data_info_tab import DataInfoTab
from Main.gui.tabs.Plot.plot_tab import PlotTab
from Main.gui.tabs.Comparison.comparison_tab import ComparisonTab
from Main.gui.tabs.Representation.representation_tab import RepresentationTab
from Main.gui.tabs.Adviser.adviser_tab import AdviserTab


class PACS(QMainWindow):
    def __init__(self, parent=None):
        super(PACS, self).__init__(parent)
        uic.loadUi("Main/main.ui", self)

        self.tabs = [
            DataInfoTab(),
            PlotTab(),
            ComparisonTab(),
            RepresentationTab(),
            AdviserTab()
        ]

        for tab in self.tabs:
            self.tab_main.addTab(tab, tab.name)

        self._data_1 = None
        self._data_2 = None

        self.load_widget = LoadWidget()

        self.connect_signals_and_slots()
        self.update_data_list()

    def connect_signals_and_slots(self):
        self.btn_load_new.clicked.connect(self.load_new_data)
        self.btn_select.clicked.connect(self.select_data)

        for tab in self.tabs:
            tab.data_update_required.connect(self.update_tabs)

    def load_new_data(self):
        self.load_widget.show()

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
            if tab.need_two_data_sets:
                tab.update_tab(self._data_1, self._data_2)
            else:
                tab.update_tab(self._data_1)

    def main(self):
        self.show()
