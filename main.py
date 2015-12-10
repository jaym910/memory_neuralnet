from memory_network import MemoryNetwork
from feedforwardNN import DirectMappingNN
from alcove import Alcove
import numpy as np
import random
from global_utils import load_phoneme_mapping
from matplotlib import pyplot as plt
from matplotlib import style
from word_distribution import *




def plot_error_per_epoch(err_per_epochs, legend_list, error_type):
    """
    args:
        err_per_epochs - should be a list of the different lines to plot
        legend_list - list of strings naming each line
        error_type - string containing type of error
    """
    plt.figure(facecolor='gray')
    x = np.array([i for i in range(1, len(err_per_epochs[0])+1)])
    for err in err_per_epochs:
        plt.plot(x, err)
    plt.xlabel("Epoch number")
    plt.ylabel(error_type)
    plt.xlim(1, x[-1])
    plt.legend(legend_list, loc='upper right')
    plt.show()


def main():
    plt.rcParams['toolbar'] = 'None'
    style.use('ggplot')
    random.seed(1)
    np.random.seed(1)
    exemplar_nodes = 100

    load_phoneme_mapping()


    present_tense_words = load_data('datasets/ipat_484.txt', 'datasets/ipat_484_present.txt')
    past_tense_words = load_data('datasets/tpat_484.txt', 'datasets/ipat_484_past.txt')

    distribution = create_distribution()

    indices = get_indices_from_dist(500,distribution)

    ipats = create_patterns(indices,present_tense_words)
    print ipats.keys()
    tpats = create_patterns(indices,past_tense_words)

    ipats_binaries = ipats.values()
    tpats_binaries = tpats.values()

    input_size = len(ipats_binaries[0])
    output_size = len(tpats_binaries[0])



    canonical = DirectMappingNN(input_size,
                                output_size=output_size,
                                l_rate=.02)
    memory = Alcove(input_size, output_size, exemplar_nodes, r=2.0,
                    o_lrate=.02, a_lrate=.02)

    memory_net = MemoryNetwork(canonical, memory, input_size, output_size,
                               error_func="cross_entropy", l_rate=.02)
    # set both routes on
    MemoryNetwork.CANONICAL_ON = True
    MemoryNetwork.MEMORY_ON = True
    #memory_net.train(ipats_binaries[:100], tpats_binaries[:100], 100)
    #epe1 = memory_net.err_per_epoch
    #plot_error_per_epoch([epe1], ['Dual route'], 'Average cross-entropy')
   


if __name__ == "__main__":
    main()
