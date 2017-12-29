from PyQt4 import uic
from PyQt4.QtGui import *

from Generator.generator import Generator
from IO.storage_manager import StorageManager
from Processor.processor import Processor
from Visualizer.visualizer import Visualizer

from IO.gui.load_widget import LoadWidget


class PACS(QMainWindow):

    def __init__(self, parent=None):
        super(PACS, self).__init__(parent)
        uic.loadUi("Main/main.ui", self)

        self.load_widget = LoadWidget()

        self.set_tab_data_info(Visualizer.get_empty())
        self.set_tab_show_data(Visualizer.get_empty())
        self.set_tab_clusterize(Visualizer.get_empty())
        self.set_tab_compare(Visualizer.get_empty())
        self.set_tab_represent(Visualizer.get_empty())
        self.set_tab_get_advise(Visualizer.get_empty())

        self.connect_signals_and_slots()

    def set_tab_data_info(self, new_widget):
        self.tab_main.insertTab(0, new_widget, "Информация")

    def set_tab_show_data(self, new_widget):
        self.tab_main.insertTab(1, new_widget, "Проекция")

    def set_tab_clusterize(self, new_widget):
        self.tab_main.insertTab(2, new_widget, "Кластеризовать")

    def set_tab_compare(self, new_widget):
        self.tab_main.insertTab(3, new_widget, "Сравнение")

    def set_tab_represent(self, new_widget):
        self.tab_main.insertTab(4, new_widget, "Представление")

    def set_tab_get_advise(self, new_widget):
        self.tab_main.insertTab(5, new_widget, "ПППР")

    def connect_signals_and_slots(self):
        self.btn_load_new.clicked.connect(self.load_new_data)

    def load_new_data(self):
        self.load_widget.show()

    def main(self):
        self.show()
