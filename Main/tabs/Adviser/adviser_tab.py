from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab
from Adviser.adviser import Adviser


class AdviserTab(AbstractVisualizationTab):
    def __init__(self, parent=None):
        ui_file = "Adviser/adviser_gui.ui"
        super(AdviserTab, self).__init__(ui_file, parent)
        self.name = "ПППР"
        self.need_two_data_sets = True
        self._data_2 = None
        self.adviser = Adviser()

        self.btn_submit.clicked.connect(self._update_tab)

    def set_text(self, decision, comment, indexes, parameters):
        self.te_decision.setText(decision)
        self.te_comment.setText(comment)
        self.te_ind.setText(indexes)
        self.te_params.setText(parameters)

    def update_tab(self, data1, data2):
        self._data = data1
        self._data_2 = data2

    def _update_tab(self):
        # TODO: spoils current data!!
        if self.choose_params.isChecked():
            advice = self.adviser.choose_params(self._data)
        elif self.compare.isChecked():
            advice = self.adviser.compare(self._data, self._data_2)
        else:
            return
        self.set_text(advice.decision, advice.comment,
                      advice.indexes, advice.params)

