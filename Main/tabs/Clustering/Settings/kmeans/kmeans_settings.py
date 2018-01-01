from Main.tabs.Clustering.Settings.abstract_settings_widget import AbstractSettingsWidget


class KmeansSettings(AbstractSettingsWidget):
    settings_for_algorithm = "k-means"

    def __init__(self):
        super(KmeansSettings, self).__init__("Main/tabs/Clustering/Settings/kmeans/kmeans_settings.ui")

    def get_settings(self):
        settings = {'num_clusters': self.n_clust.value()}
        return settings
