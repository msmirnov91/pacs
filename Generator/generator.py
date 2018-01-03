import re

import numpy as np
import pandas as pd

from Common.data import Data


class Generator(object):
    @classmethod
    def generate(cls, settings):
        if settings == "":
            raise Exception("No settings received!")
        cluster_descriptions = settings.split(' ')
        elements = pd.DataFrame()

        for i in range(0, len(cluster_descriptions)):
            description = cluster_descriptions[i]
            # get the form of cluster
            form = description[0]

            # search first digit en description(amount of elements)
            match = re.search("\d+", description)
            capacity = (int(match.group(0)))

            # search in description construction (means)(sigmas)
            match = re.search('\((?P<means>.+)\)\((?P<sigmas>.+)\)', description)
            # two lists below contains string objects
            means_str = match.group('means').split(',')
            sigmas_str = match.group('sigmas').split(',')

            # convert string-array to float-array
            means = []
            sigmas = []
            for m, s in zip(means_str, sigmas_str):
                means.append(float(m))
                sigmas.append(float(s))

            dimension = len(means)
            if dimension != len(sigmas):
                raise Exception("Wrong dimension!")

            if form == 'e':
                distribution_law = np.random.normal
                first_args = means
                second_args = sigmas
            elif form == 'r':
                distribution_law = np.random.uniform
                first_args = []
                second_args = []
                for mean, sigma in zip(means, sigmas):
                    first_args.append(mean - sigma)
                    second_args.append(mean + sigma)
            else:
                raise Exception('Unknown distribution law')

            # generate data column by column
            cluster = None
            column_size = (capacity, 1)
            for j in range(0, dimension):
                coord_name = "x{}".format(j)
                first_arg = int(first_args[j])
                second_arg = int(second_args[j])
                column = pd.DataFrame(distribution_law(first_arg, second_arg, column_size), columns=[coord_name])

                if cluster is None:
                    cluster = column
                else:
                    cluster[coord_name] = column

            labels = np.ndarray(column_size, dtype=int)
            labels.fill(i)
            cluster['cls'] = labels

            elements = elements.append(cluster)
        elements = elements.set_index(Data.LABELS_COLUMN_NAME)

        data = Data('generated data')
        data.set_data(elements)

        return data


