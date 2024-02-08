from multiprocessing import Pool
import numpy as np
import matplotlib as mpl

mpl.use("agg")
import matplotlib.pyplot as plt

rand_size = 500
num_cores = 12


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


if __name__ == "__main__":
    with Pool(num_cores) as p:
        p.map(f, np.arange(0, 20))
