from os.path import join
from math import ceil
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 14
plt.rcParams["figure.figsize"] = [15, 8]

class reporter:

    def __init__(self, name, folder, counts, interactive=True):


        plt.subplot(221)
        plt.title("Histogram")
        sns.distplot(counts)
        plt.subplot(222)
        plt.title("Boxplot")
        plt.boxplot(counts)

        plt.subplot(223)
        clist = [ceil(c) for c in counts]
        clist = np.array(sorted(clist))
        integers = np.unique([int(c) for c in clist])
        cdf = np.array([sum(clist <= i)/len(clist) for i in integers])
        plt.title("CDF - P(x $\leq$ X)")
        plt.grid(alpha=0.25)
        plt.plot(cdf)


        plt.subplot(224)
        plt.plot(1 - cdf)
        plt.title("CCDF - P(x > X)")
        plt.grid(alpha=0.25)

        plt.suptitle(name)
        plt.savefig(join(folder, name))
        plt.clf()

        if interactive:
            import pygal as pg

            box_plot = pg.Box()
            box_plot.title = name
            box_plot.add("Values", counts)
            boxplot_name = name + "_boxplot.svg"
            box_plot.render_to_file(join(folder, boxplot_name))

            hist = pg.Bar(show_x_labels=False)
            clist = [ceil(c) for c in counts]
            freqs = [clist.count(i) for i in range(0, int(max(clist)))]
            hist.add("Values", freqs)
            hist.title = name
            hist.x_labels = map(str, integers)
            histogram_name = name + "_histogram.svg"
            hist.render_to_file(join(folder, histogram_name))

            line = pg.Line()
            line.title = name
            line.add("CDF", cdf)
            line.add("CCDF", 1 - cdf)
            line.x_labels = map(str, integers)
            # line.x_labels = map(str, counts)
            line_name = name + "_cdf_ccdf.svg"
            line.render_to_file(join(folder, line_name))

            with open(join(folder, "report_{}.html".format(name)), "w+") as out:
                obj0 = "<object type='image/svg+xml' data='"
                obj1 = "'></object>\n"
                out.write("<html><head align='center'>Report - {}</head><body>\n".format(name))
                out.write("{}{}{}".format(obj0, boxplot_name, obj1))
                out.write("{}{}{}".format(obj0, histogram_name, obj1))
                out.write("{}{}{}".format(obj0, line_name, obj1))
                out.write("</body></html>")



