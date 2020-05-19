from os.path import join, exists, isdir
from os import mkdir


class mex:

    def __init__(self, fname, out_folder, t, d, r):
        self.trace_name = fname
        self.out_folder = out_folder
        self.metrics = self.__list_metrics() 
        self.t = t
        self.d = d
        self.r = r

        if out_folder[-1] == "/" or out_folder[-1] == "\\":
            out_folder = out_folder[:-1]
        self.metrics_output_folder = "{}_metrics".format(out_folder)
        if not exists(self.metrics_output_folder):
            mkdir(self.metrics_output_folder)

        self.__execute()

    def __list_metrics(self):
        if exists("metrics.txt"):
            with open("metrics.txt", "r") as inn:
                return [metric.strip() for metric in inn if metric[0] != "#"]
        else:
            metrics = ["stayPointCount", "stayPointDuration",
                       "stayPointSignature", "stayPointUniqueEntropy"]
            with open("metrics.txt", "w+") as out:
                for m in metrics:
                    out.write("{}\n".format(m))
            return metrics

    def __execute(self):
        for m in self.metrics:
            metric_class = __import__("Metrics.{}".format(m))
            metric_class = getattr(metric_class, m)
            metric_class = getattr(metric_class, m)

            obj = metric_class(self.out_folder, self.metrics_output_folder)
            print("Running metric {}.".format(m))
            obj.extract()
            obj.save()
            obj.report()
