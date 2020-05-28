from os.path import join, exists, isdir
from os import mkdir
import argparse
from collections import namedtuple
import pandas as pd
from haversine import haversine
from mex import mex

stayPoint = namedtuple("StayPoint", ["Lat", "Lon", "Arrival", "Departure"])

class spex:

    def __init__(self):
        parsed_args = self.__parse_args()
        self.fname, self.act, self.out_folder, self.t, self.r, self.d = parsed_args
        self.t = self.t if self.t != -1 else 30
        self.r = self.r if self.r != -1 else 500
        self.d = self.d if self.d != "" else "haversine"

        if not exists(self.out_folder) or not isdir(self.out_folder):
            mkdir(self.out_folder)




    def __parse_args(self):
        desc = """
            SPEX: Stay Point EXtractor.

        """
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument("filename",
                            help="Trace file name")
        parser.add_argument("output_location",
                            help="Output folder location")
        parser.add_argument("--action", required=True,
                            help="Choose what action to do.",
                            choices=["extract_points",
                                     "extract_metrics",
                                     "extract_both"])
        parser.add_argument("-t", nargs="?",
                            help="Time threshold (in minutes)",
                            const=30, default=30, type=int)
        parser.add_argument("-d", nargs="?",
                            help="Distance function (haversine or euclidean)",
                            const="haversine", default="haversine",
                            choices=["haversine", "euclidean"])
        parser.add_argument("-r", nargs="?",
                            help="Radius threshold (in meters)",
                            const=500, default=500, type=int)

        parsed = parser.parse_args()

        fname = parsed.filename
        action = parsed.action
        output_folder = parsed.output_location
        t_value = parsed.t
        d_value = parsed.d
        r_value = parsed.r
        return fname, action, output_folder, t_value, r_value, d_value


    def load_trace(self):
        df = pd.read_csv(self.fname)
        for required in ["userid", "latitude", "longitude", "time"]:
            if required not in df.columns:
                SystemError("Column {} missing from trace.".format(required))
        df.sort_values(by="time", inplace=True)
        self.trace = df

    def __get_point(self, i):
        return (self.trace.loc[i, "latitude"], self.trace.loc[i, "longitude"])

    def __euclidean(self, a, b):
        return pow(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2), 1/2)

    def __haversine(self, a, b):
        return haversine(a, b) * 1000

    def __dist(self, a, b):
        if self.d == "haversine":
            return self.__haversine(a, b)
        elif self.d == "euclidean":
            return self.__euclidean(a, b)
        else:
            SystemError("Distance function {} not defined.".format(self.d))

    def get_staypoints(self, data):
        time_in_sec = self.t * 60
        stay_points = []
        i, j = 0, 0
        point_i = self.__get_point(i)
        point_num = len(data)
        while i < point_num:
            j = i + 1
            point_j = self.__get_point(j)
            while j < point_num:
                point_j = self.__get_point(j)
                d = self.__dist(point_i, point_j)
                if d > self.r:
                    delta_t = data.loc[j, "time"] - data.loc[i, "time"]
                    if delta_t > time_in_sec:
                        sp = stayPoint(Lat=data.loc[i:(j+1), "latitude"].mean(),
                                       Lon=data.loc[i:(j+1), "longitude"].mean(),
                                       Arrival=data.loc[i, "time"],
                                       Departure=data.loc[j, "time"])
                        stay_points.append(sp)
                    i = j
                    point_i = self.__get_point(i)
                    break
                j = j + 1
            if j >= point_num - 1:
                break
        return stay_points


    def extract_by_user(self):
        number_of_users = len(self.trace.userid.unique())
        for idx, (uname, udata) in enumerate(self.trace.groupby("userid"), 1):
            s = "\rProcessing user with id #{} ({} of {})"
            print(s.format(uname, idx, number_of_users), end="")

            ud = udata.reset_index(drop=True)
            stay_points = self.get_staypoints(ud)

            out_filename = "{}_stay_points.csv".format(uname)
            out_location = join(self.out_folder, out_filename)

            with open(out_location, "w+") as out:
                out.write("latitude,longitude,arrival,departure\n")
                for sp in stay_points:
                    out.write("{},{},{},{}\n".format(sp.Lat, sp.Lon,
                                                   sp.Arrival, sp.Departure))


if __name__ == "__main__":
    e = spex()
    if e.act == "extract_trace":
        e.load_trace()
        e.extract_by_user()
    elif e.act == "extract_metrics":
        mex(e.fname, e.out_folder, e.t, e.d, e.r)
    else:
        e.load_trace()
        e.extract_by_user()
        mex(e.fname, e.out_folder, e.t, e.d, e.r)

