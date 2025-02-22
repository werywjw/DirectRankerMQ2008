from __future__ import print_function

import sys
import numpy as np

sys.path.append('..')
import tensorflow as tf
import DirectRanker as drr
import helpers as hlps
#from DirectRankerMQ2008.DirectRanker import directRanker
#from DirectRankerMQ2008.helpers import readData
import timeit

import warnings
warnings.filterwarnings("ignore")

# CHANGE THE DATA PATH!!!
# Change number_features to 46 and binary=False for MQ2007/8 and 136 and binary=True for MSLR
# x_train, y_train, q_train = readData(data_path="../data/MSLR-WEB10K/Fold1/train.txt", binary=True, at=10, number_features=136, bin_cutoff=1.5, cut_zeros=True)
# For debugging
x_train, y_train, q_train = hlps.readData(debug_data=True, binary=True, at=10, number_features=136, bin_cutoff=1.5,
                                     cut_zeros=True)
# x_test, y_test, q_test = readData(data_path="../data/MSLR-WEB10K/Fold1/test.txt", binary=True, at=10, number_features=136, bin_cutoff=1.5, cut_zeros=True)
# For debugging
x_test, y_test, q_test = hlps.readData(debug_data=True, binary=True, at=10, number_features=136, bin_cutoff=1.5,
                                  cut_zeros=True)

time_dr = []
time_rank = []

def ranknet_cost(nn, y0):
    return tf.reduce_mean(tf.log(1+tf.exp((1+nn)/2))-(1+nn)/2)

for i in range(10):

    # Load directRanker, train, and test
    dr = drr.directRanker(
        feature_activation=tf.nn.tanh,
        ranking_activation=tf.nn.tanh,
        # max_steps=10000,
        # For debugging
        max_steps=5000,
        print_step=500,
        start_batch_size=3,
        end_batch_size=5,
        start_qids=20,
        end_qids=100,
        feature_bias=True,
        hidden_layers=[30, 5]
    )

    ranknet = drr.directRanker(
        feature_activation=tf.nn.relu,
        ranking_activation=tf.nn.tanh,
        # max_steps=10000,
        # For debugging
        max_steps=5000,
        print_step=500,
        optimizer=tf.train.GradientDescentOptimizer,
        start_batch_size=3,
        end_batch_size=5,
        start_qids=20,
        end_qids=100,
        feature_bias=True,
        cost=ranknet_cost,
        hidden_layers=[30, 5]
    )

    start = timeit.default_timer()
    ranknet.fit(x_train, y_train, ranking=True)
    stop = timeit.default_timer()
    time_rank.append(stop - start)
    print('Time RankNet: ', stop - start)

    start = timeit.default_timer()
    dr.fit(x_train, y_train, ranking=True)
    stop = timeit.default_timer()
    time_dr.append(stop - start)
    print('Time DirectRanker: ', stop - start)

print('Mean Time DirectRanker: ' + np.mean(time_dr) + " +- " + np.std(time_dr))
print('Mean Time RankNet: ' + np.mean(time_rank) + " +- " + np.std(time_rank))

# wery@Werys-MBP DirectRankerMQ2008 %  cd /Users/wery/Desktop/DirectRankerMQ2008 ; /usr/bin/env /usr/bin/python3 /Users/wery/.vscode/extensions/ms-python.p
# ython-2022.20.2/pythonFiles/lib/python/debugpy/adapter/../../debugpy/launcher 52169 -- /Users/wery/Desktop/DirectRankerMQ2008/run_time.py 
# Traceback (most recent call last):
#   File "/Users/wery/Desktop/DirectRankerMQ2008/run_time.py", line 56, in <module>
#     optimizer=tf.train.GradientDescentOptimizer,
# AttributeError: module 'tensorflow._api.v2.train' has no attribute 'GradientDescentOptimizer'