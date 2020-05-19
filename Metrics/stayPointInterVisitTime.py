from os import listdir
from os.path import isfile, join
from datetime import datetime
import pandas as pd
from haversine import haversine
from Metrics.reporter import reporter

class stayPointInterVisitTime:

    def __init__(self, folder, output_folder):
        self.folder = folder
        self.fnames = [f for f in listdir(folder) if isfile(join(folder, f))]
        self.output_file = join(output_folder, "stayPointInterVisitTime")
        self.output_folder = output_folder

    def extract(self):
        default_time = 1391212800
        inter_times = []
        for fname in self.fnames:
            df = pd.read_csv(join(self.folder, fname))
            locs = {}
            for tup in df.itertuples():
                point = (tup.latitude, tup.longitude)
                locs, it = self.find_similar(locs, point,
                                             tup.arrival, tup.departure)
                if it != 0:
                    inter_times.append(it)
        self.inter_times = [i/3600 for i in inter_times if i/3600 < 24]
        return inter_times

    def find_similar(self, locations, point, arrival, departure):
        current_key = len(locations)
        found = False
        inter_time = 0
        if len(locations) == 0:
            locations[current_key] = [point, departure]
        else:
            for key, item in locations.items():
                item_loc = item[0]
                if haversine(point, item_loc) <= 0.05:
                    inter_time = arrival - locations[key][1]
                    new_x = (point[0] + item_loc[0])/2
                    new_y = (point[1] + item_loc[1])/2
                    locations[key] = [(new_x, new_y), departure]
                    found = True
                    break
            if not found:
                locations[current_key] = [point, departure]
        return locations, inter_time

    def save(self):
        with open(self.output_file, "w+") as out:
            for c in self.inter_times:
                out.write("{}\n".format(c))

    def report(self):
        reporter("stayPointInterVisitTime", self.output_folder, self.inter_times)
