from PyQt4.QtGui import QLabel


class EmptyWidget(QLabel):
    TEXT = "Данные не выбраны"

    def __init__(self, parent=None):
        super(EmptyWidget, self).__init__(parent)
        self.setText(self.TEXT)
