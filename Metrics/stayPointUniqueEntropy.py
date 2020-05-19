from os import listdir
from os.path import isfile, join
from datetime import datetime
from math import log
import pandas as pd
from haversine import haversine
from Metrics.reporter import reporter

SIMILARITY_RADIUS = .1

class stayPointUniqueEntropy:

    def __init__(self, folder, output_folder):
        self.folder = folder
        self.fnames = [f for f in listdir(folder) if isfile(join(folder, f))]
        self.output_file = join(output_folder, "stayPointUniqueEntropy")
        self.output_folder = output_folder

    def extract(self):
        default_time = 1391212800  # Only appliable to Rome
        counts = []
        entropies = []
        for fname in self.fnames:
            df = pd.read_csv(join(self.folder, fname))
            locs = {}
            for tup in df.itertuples():
                point = (tup.latitude, tup.longitude)
                locs = self.__find_similar(locs, point)
            counts += [item[1] for item in locs.values()]
            if locs:
                entropies.append(self.__extract_entropy(locs))
        self.entropies = entropies
        return counts, entropies

    def __find_similar(self, locations, point):
        current_key = len(locations)
        found = False
        if len(locations) == 0:
            locations[current_key] = [point, 1]
        else:
            for key, item in locations.items():
                item_loc = item[0]
                item_count = item[1]
                if haversine(point, item_loc) <= SIMILARITY_RADIUS:
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
        entropy_max = round(entropy_max, 2)
        entropy = round(entropy, 2)
        if entropy > entropy_max:
            print("Entropy max is {}, entropy is {}".format(entropy_max, entropy))
        return entropy/max(entropy_max, 1)

    def save(self):
        with open(self.output_file, "w+") as out:
            for c in self.entropies:
                out.write("{}\n".format(c))

    def report(self):
        reporter("stayPointUniqueEntropy", self.output_folder, self.entropies)
