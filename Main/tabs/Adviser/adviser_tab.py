from Main.tabs.abstract_visualization_tab import AbstractVisualizationTab


class AdviserTab(AbstractVisualizationTab):
    def __init__(self, parent=None):
        ui_file = "Adviser/adviser_gui.ui"
        super(AdviserTab, self).__init__(ui_file, parent)
        self.name = "ПППР"
        self.index_report = ""

    def create_index_report(self, names, indexes):
        report = ""
        for name, index in zip(names, indexes):
            index_str = self.index_val_pattern.format(index)
            report += name + ": " + index_str + '\n'
        self.index_report = report

    def set_text(self, decision, comment, parameters):
        self.te_decision.setText(decision)
        self.te_comment.setText(comment)
        self.te_ind.setText(self.index_report)
        self.te_params.setText(parameters)
