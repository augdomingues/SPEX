from os import listdir
from os.path import isfile, join
from datetime import datetime
from math import log
import pandas as pd
from haversine import haversine
from Metrics.reporter import reporter

SIMILARITY_RADIUS = .1

class stayPointGeneralEntropy:

    def __init__(self, folder, output_folder, *args):
        self.folder = folder
        self.fnames = [f for f in listdir(folder) if isfile(join(folder, f))]
        self.output_file = join(output_folder, "stayPointGeneralEntropy")
        self.output_folder = output_folder
        self.dist_func = args[0]


    def extract(self):
        entropies = []
        locs = {}
        for fname in self.fnames:
            df = pd.read_csv(join(self.folder, fname))
            for tup in df.itertuples():
                point = (tup.latitude, tup.longitude)
                locs = self.__find_similar(locs, point)
        entropies.append(self.__extract_entropy(locs))
        self.entropies = entropies
        return entropies

    def __dist_func(self, a, b):
        if self.dist_func == "euclidean":
            return pow(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2), 1/2)
        elif self.dist_func == "haversine":
            return haversine(a, b)

    def __find_similar(self, locations, point):
        current_key = len(locations)
        found = False
        if len(locations) == 0:
            locations[current_key] = [point, 1]
        else:
            for key, item in locations.items():
                item_loc = item[0]
                item_count = item[1]
                if self.__dist_func(point, item_loc) <= SIMILARITY_RADIUS:
                    new_x = (point[0] + item_loc[0])/2
                    new_y = (point[1] + item_loc[1])/2
                    locations[key] = [(new_x, new_y), item_count + 1]
                    found = True
                    break
            if not found:
                locations[current_key] = [point, 1]
        return locations

    def __extract_entropy(self, locations):
        total = sum([item[1] for item in locations.values()])
        entropy = 0
        for v in locations.values():
            prob_v = v[1]/total
            entropy += prob_v*log(1/prob_v, 2)

        num_loc = len(locations)
        prob_uniform = 1/num_loc
        entropy_max = num_loc * (prob_uniform)*log(1/prob_uniform, 2)
        if entropy > entropy_max:
            print("Entropy max is {}, entropy is {}".format(entropy_max, entropy))
        return entropy/max(entropy_max, 1)

    def save(self):
        with open(self.output_file, "w+") as out:
            for c in self.entropies:
                out.write("{}\n".format(c))

    def report(self):
        pass
