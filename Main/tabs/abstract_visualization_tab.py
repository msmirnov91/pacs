from Main.tabs.abstract_tab import AbstractTab
from Visualizer.visualizer import Visualizer


class AbstractVisualizationTab(AbstractTab):
    def __init__(self, ui_file, parent=None):
        super(AbstractVisualizationTab, self).__init__(ui_file, parent)
        self.need_two_data_sets = False
        self.index_val_pattern = "{:4.2f}"
        self._data = None

        self.is_visualization_tab = True
        self.visualizer = Visualizer()

    def change_visualization_widget_to(self, new_widget):
        self._change_widget_on_layout_to(self.plot_layout, new_widget)

    def get_plot_widget(self):
        # curr_widget_item = self.plot_layout.takeAt(0)
        curr_widget_item = self.plot_layout.itemAt(0)
        if curr_widget_item is not None:
            return curr_widget_item.widget()
        else:
            return None

    def update_tab(self, data):
        self._data = data
        self._update_tab()

    def _update_tab(self):
        pass

    def add_image_to_report(self, report_dir, img_number):
        plot_widget = self.get_plot_widget()
        img_name = "{}{}.png".format(plot_widget.image_name, img_number)
        plot_widget.save_image(report_dir, img_name)
        return img_name

    def get_plot_name(self):
        return self.get_plot_widget().image_name

    def get_description_for_report(self):
        return None

