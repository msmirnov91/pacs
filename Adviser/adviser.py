from Processor.processor import Processor
from Adviser.advice import Advice


class Adviser(object):
    def choose_params(self, data):
        if data is None:
            return self.lack_of_data_notification()

        advice = Advice()

        eps = self.calc_eps(data)
        min_samples = self.calc_min_samples(data, eps)

        dbscan_settings = {'eps': eps,
                           'min_samples': min_samples}

        labels = Processor().get_cluster_labels(data, "dbscan", dbscan_settings)
        data.set_labels(labels)

        ind_1 = Processor.get_silhouette(data)

        n_clust = data.clusters_amount()
        kmeans_settings = {'num_clusters': n_clust}
        labels = Processor().get_cluster_labels(data, "k-means", kmeans_settings)
        data.set_labels(labels)

        ind_2 = Processor.get_silhouette(data)

        if ind_1 > ind_2:
            decision = "Предпочтительнее алгоритм DBSCAN " \
                       "с параметрами eps={} min_samples = {}".format(eps, min_samples)
            comment = "Индекс силуэт показал большее значение для алгоритма DBSCAN"
        elif ind_2 > ind_1:
            decision = "Предпочтительнее алгоритм k-means" \
                       "с числом кластеров {}".format(n_clust)
            comment = "Индекс силуэт показал большее значение для алгоритма k-means"
        elif ind_1 == ind_2:
            decision = "Оба варианта равнозначны"
            comment = "В обоих случаях индексы оказались одинаковыми"
        else:
            decision = "Неопределенная ситуация"
            comment = "Невозможно сделать вывод по индексам"

        index_names = ['Silhouette1', 'Silhouette2']

        index_vals = [ind_1, ind_2]

        indexes = self.create_index_report(index_names, index_vals)
        parameters = "eps: {}\n" \
                     "min_samples: {}\n" \
                     "n_clust: {}\n".format(eps, min_samples, n_clust)

        advice.decision = decision
        advice.comment = comment
        advice.indexes = indexes
        advice.params = parameters
        return advice

    def compare(self, data1, data2):
        if data1 is None or data2 is None:
            return self.lack_of_data_notification()

        advice = Advice()

        ami = Processor().get_ami(data1, data2)
        ari = Processor().get_ari(data1, data2)

        threshold_max = 0.8
        threshold_min = 0.4
        index_delta = 0.3

        if ari > threshold_max and ami > threshold_max:
            decision = "Кластеризации практически идентичны"
            comment = "Оба индекса  показали высокие значения"
        elif ari < threshold_min and ami < threshold_min:
            decision = "Кластеризации существенно отличаются"
            comment = "Оба индекса показали низкие значения"
        elif abs(ari - ami) > index_delta:
            decision = "Индексы дают протворечивый результат"
            comment = "Индексы слишком отличаются, затруднительно дать однозначный ответ"
        else:
            decision = "Наблюдается определенное сходство кластеризаций"
            comment = "Значение обоих индексов достаточно велико и непротиворечиво"

        index_names = [
            'Adj rand',
            'Adj mutual info'
        ]

        index_vals = [
            ari,
            ami
        ]
        indexes = self.create_index_report(index_names, index_vals)
        parameters = "threshold_max: {}\n" \
                     "threshold_min: {}\n" \
                     "index_delta: {}\n".format(threshold_max, threshold_min, index_delta)

        advice.decision = decision
        advice.comment = comment
        advice.indexes = indexes
        advice.params = parameters
        return advice

    @classmethod
    def calc_eps(cls, data):
        # TODO: make implementaton!!
        return 0.2

    @classmethod
    def calc_min_samples(cls, data, eps):
        # TODO: make implementaton!!
        return 10

    @classmethod
    def create_index_report(cls, names, indexes):
        report = ""
        for name, index in zip(names, indexes):
            index_str = "{:4.2f}".format(index)
            report += name + ": " + index_str + '\n'
        return report

    @classmethod
    def lack_of_data_notification(cls):
        advice = Advice()

        advice.decision = "Невозможно принять решение"
        advice.comment = "Выбрано мало данных"
        return advice
