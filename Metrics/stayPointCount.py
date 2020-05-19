"""
    stayPointCount: extracts and returns the distribution of number of stay
    points per user
"""
from os import listdir
from os.path import isfile, join
from Metrics.reporter import reporter

class stayPointCount:

    def __init__(self, folder, output_folder):
        self.folder = folder
        self.fnames = [f for f in listdir(folder) if isfile(join(folder, f))]
        self.output_file = join(output_folder, "stayPointCount")
        self.output_folder = output_folder

    def extract(self):
        """
            extract: access each user file and returns the total of
            stay points.
        """
        counts = []
        for fname in self.fnames:
            with open(join(self.folder, fname), "r") as inn:
                inn.readline()  # Jump header
                for count, _ in enumerate(inn, 1):
                    pass
                counts.append(count)
        self.counts = counts
        return counts


    def save(self):
        with open(self.output_file, "w+") as out:
            for c in self.counts:
                out.write("{}\n".format(c))

    def report(self):
        reporter("stayPointCount", self.output_folder, self.counts)
