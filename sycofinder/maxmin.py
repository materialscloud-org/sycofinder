#! /usr/bin/env python

##################################
# this program generates a diverse set of individuals for initializing GA.
# It uses max-min algorithm to find the most diverse set.
# Easily you can modify it for other needs.
# Mohamad Moosavi 13Dec 2017
##################################

from __future__ import print_function
import numpy as np
import itertools
import time


def check_sample(a, var_LB, var_UB):
    # this function check if the randomely generated sample point
    # lies on the phase space. In other words, it applies the constraints.
    # For example, the volume of solvent in our study should not be above 6ml.
    a = np.asarray(a)
    a = np.multiply(a, (var_UB - var_LB)) + var_LB
    vol = np.sum(a[4:9])
    cond = vol <= 6 and vol >= 1  # pylint: disable=chained-comparison

    return cond


def compute_distance(x, y, w):
    # This function compute the pairwise distance between two vectors.
    # It weigths the distance based on the importance of variables.
    return np.linalg.norm(w * (x - y))


def min_max(nsamples, NPS, var_importance):
    # This function returns the most diverse set of parameters weighted with variable importance.
    selected_indices = []
    selected_set = [np.zeros([1, NPS.shape[1]])]  # the selected points

    prtime_start = time.time()
    prtime = time.time()
    while len(selected_set) <= nsamples:
        distances = np.zeros([NPS.shape[0], 1])
        for i, psamp in enumerate(NPS):
            min_dist = 100000000
            for samp in selected_set:
                d = compute_distance(samp, psamp, var_importance)
                if d < min_dist:
                    min_dist = d

            distances[i] = min_dist
        extime = time.time() - prtime
        prtime = time.time()
        print((np.argmax(distances), distances[np.argmax(distances)],
               " execution time for current landmark: ", extime))
        selected_indices.append(np.argmax(distances))
        selected_set.append(NPS[np.argmax(distances), :])
    print(("Total execution time of MaxMin: ", time.time() - prtime_start))
    return selected_set, selected_indices


def compute(var_importance,
            var_LB,
            var_UB,
            method,
            num_samples=10,
            ngrids_per_dim=5):
    """Compute most diverse set of inputs.

    :param var_importance: list of weights
    :param var_LB: list of lower bounds
    :param var_UB: list of upper bounds
    :param method: which method to use
    :param num_samples: number of samples to pick
    :param ngrids_per_dim: number of grid points in each variable

    :return result: String containing coordinates of sample points.
    """
    num_variables = len(var_importance)

    if method == 'primitive':
        grids_dim = np.linspace(
            0,
            1,
            num=ngrids_per_dim,
            endpoint=True,
        )
        print(("On each dimension, we sample: ", grids_dim))
        NPS1 = itertools.product(grids_dim, repeat=num_variables)
        #NPS1=[np.array(i) for i in NPS1 if check_sample(i,var_LB,var_UB)]
        NPS1 = [np.array(i) for i in NPS1]
        NPS1 = np.asarray(NPS1)
        print(("In total, there are ", len(NPS1), "samples in the space\n"))

        norm_diverse_set, sel_ind = min_max([], num_samples, NPS1,
                                            var_importance)
        print(norm_diverse_set)
        coords = NPS1[sel_ind]

    elif method == 'convex-opt':
        from .maxmin_dccp import max_min_dccp
        coords = max_min_dccp(num_samples, var_importance)

    else:
        raise ValueError("Unknown method {}".format(method))

    diverse_set = np.multiply(coords, var_UB - var_LB) + var_LB

    return diverse_set
