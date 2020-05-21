from os import listdir
from os.path import isfile, join
from datetime import datetime
from collections import defaultdict
from math import log
import pandas as pd
from haversine import haversine
from Metrics.reporter import reporter

SIMILARITY_RADIUS = .1


class stayPointGraph:

    def __init__(self, folder, output_folder, *args):
        self.folder = folder
        self.fnames = [f for f in listdir(folder) if isfile(join(folder, f))]
        self.output_file = join(output_folder, "stayPointGraph")
        self.output_folder = output_folder
        self.dist_func = args[0]

    def extract(self):
        visits = {}
        locs = {}
        for fname in self.fnames:
            username = fname.replace("stay_points", "").replace(".csv", "").replace("_", "")
            visits[username] = dict()
            df = pd.read_csv(join(self.folder, fname))
            for tup in df.itertuples():
                point = (tup.latitude, tup.longitude)
                locs, ck = self.__find_similar(locs, point)
                if ck not in visits[username]:
                    visits[username][ck] = 0
                visits[username][ck] += 1
        self.visits = visits
        self.locations = locs
        return visits

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
                    current_key = key
                    found = True
                    break
            if not found:
                locations[current_key] = [point, 1]
        return locations, current_key


    def save(self):
        with open(self.output_file + "_locs", "w+") as out:
            out.write("locid,latitude,longitude,count\n")
            for key, v in self.locations.items():
                out.write("{},{},{},{}\n".format(key, v[0][0], v[0][1], v[1]))

        with open(self.output_file + "_visits", "w+") as out:
            out.write("userid,locid,count\n")
            for key, value in self.visits.items():
                for loc, count in value.items():
                    out.write("{},{},{}\n".format(key, loc, count))

    def report(self):
        pass
