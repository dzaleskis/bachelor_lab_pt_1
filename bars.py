import os

import numpy
from matplotlib import pyplot as plt

distribution_names = {
    "shuffled_int": "Atsitiktiniai",
    "shuffled_16_values_int": "Atsitiktiniai (16 reikšmių)",
    "ascending_int": "Didėjantys",
    "descending_int": "Mažėjantys",
    "pipe_organ_int": "Vargonai",
    "partially_sorted_int": "Pusė išrikiuota",
}

sort_order = ["pdqsort", "ips4o", "timsort", "std::sort", "std::stable_sort", "std::sort_heap"]

for filename in os.listdir("profiles"):
    data = {}
    for line in open(os.path.join("profiles", filename)):
        size, distribution, algo, *results = line.split()
        size = float(size)
        distribution = distribution_names[distribution]
        results = [float(result) for result in results]
        if not size in data: data[size] = {}
        if not distribution in data[size]: data[size][distribution] = {}
        data[size][distribution][algo] = results

    for size in data:
        distributions = list(distribution_names.values())

        algos = tuple(data[size][distributions[0]].keys())
        algos = tuple(sorted(algos, key=lambda a: sort_order.index(a) if a in sort_order else 1000))

        groupnames = distributions
        groupsize = len(algos)
        groups = [[data[size][distribution][algo] for algo in algos] for distribution in distributions]
        barwidth = 0.6
        spacing = 1
        groupwidth = groupsize * barwidth + spacing

        colors = ["#aec7e8", "#1f77b4", "#484c66", "#ffbb78", "#ff7f0e", "#800080"]
        for i, algo in enumerate(algos):
            heights = [numpy.median(data[size][distribution][algo]) for distribution in distributions]
            errors = [numpy.std(data[size][distribution][algo]) for distribution in distributions]
            plt.barh([barwidth*i + groupwidth*n for n in range(len(distributions))],
                     heights, 0.6, color = colors[i], label = algo)

        # Set axes limits and labels.
        plt.yticks([barwidth * groupsize/2 + groupwidth*n for n in range(len(groupnames))], groupnames)
        plt.xlabel("ns / n log n")

        # Turn off ticks for y-axis.
        plt.tick_params(
            axis="y",
            which="both",
            left="off",
            right="off",
            labelleft="on"
        )

        ax = plt.gca()
        ax.invert_yaxis()
        ax.relim()
        ax.autoscale_view()
        plt.ylim(plt.ylim()[0]+1, plt.ylim()[1]-1)
        plt.legend(loc="right", fontsize=10)

        figure = plt.gcf()
        figure.set_size_inches(8*.75, 6*.75)
        plt.savefig(os.path.join("plots", "{}_{}.png".format(os.path.splitext(filename)[0], int(size))),
                    dpi = 200, bbox_inches="tight")

        plt.clf()
