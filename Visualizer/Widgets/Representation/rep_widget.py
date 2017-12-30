from GUI.matplotlib_widget import MatplotlibWidget


class RepWidget(MatplotlibWidget):
    def __init__(self, splitting, parent=None):
        self.splitting = splitting
        super(RepWidget, self).__init__(parent)

    def update_splitting(self, new_splitting):
        self.splitting = new_splitting
        self.redraw()
