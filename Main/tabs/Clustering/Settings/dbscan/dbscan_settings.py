from Main.tabs.Clustering.Settings.abstract_settings_widget import AbstractSettingsWidget


class DbscanSettings(AbstractSettingsWidget):
    settings_for_algorithm = "dbscan"

    def __init__(self):
        super(DbscanSettings, self).__init__("Main/tabs/Clustering/Settings/dbscan/dbscan_settings.ui")

    def get_settings(self):
        settings = {'eps': self.eps.value(),
                    'min_samples': self.min_samples.value()}
        return settings
