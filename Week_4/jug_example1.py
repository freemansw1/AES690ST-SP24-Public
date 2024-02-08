import jug
import numpy as np
import matplotlib as mpl

mpl.use("agg")
import matplotlib.pyplot as plt

rand_size = 500
num_cores = 10


@jug.TaskGenerator
def f(seed):
    # set seed
    np.random.seed(seed)
    # generate random data
    plot_data = np.random.rand(rand_size, rand_size)
    cm = plt.pcolormesh(plot_data)
    plt.colorbar(cm)
    plt.title("Random data, seed: {0}".format(seed))
    plt.savefig("./rand_figs/rand_fig_{0}.png".format(seed))
    return seed


out_list = list()
for seed_num in np.arange(0, 20):
    out_list.append(f(seed_num))
