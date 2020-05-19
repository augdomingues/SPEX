from os import listdir
from os.path import isfile, join
import pandas as pd
from Metrics.reporter import reporter

class stayPointDuration:

    def __init__(self, folder, output_folder):
        self.folder = folder
        self.fnames = [f for f in listdir(folder) if isfile(join(folder, f))]
        self.output_file = join(output_folder, "stayPointDuration")
        self.output_folder = output_folder

    def extract(self):
        counts = []
        for fname in self.fnames:
            df = pd.read_csv(join(self.folder, fname))
            counts += list((df.departure - df.arrival)/3600)
        self.counts = [c for c in counts if c <= 24]
        return counts

    def save(self):
        with open(self.output_file, "w+") as out:
            for c in self.counts:
                out.write("{}\n".format(c))

    def report(self):
        reporter("stayPointDuration", self.output_folder, self.counts)
