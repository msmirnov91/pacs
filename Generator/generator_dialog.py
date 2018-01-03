from PyQt4 import uic
from PyQt4.QtGui import QDialog

from Generator.generator import Generator
from IO.gui.save_widget import SaveWidget
from Main.tabs.Plot.plot_tab import PlotTab


class GeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super(GeneratorDialog, self).__init__(parent)
        uic.loadUi("Generator/generator_dialog.ui", self)
        self.plot_tab = PlotTab()
        self._data = None

        self.plot_layout.addWidget(self.plot_tab)
        self.btn_generate.clicked.connect(self.generate)

    def generate(self):
        description = self.le_description.text()
        self._data = Generator().generate(description)
        self.plot_tab.update_tab(self._data)

    def accept(self):
        save_widget = SaveWidget(self._data)
        return save_widget.exec_()
