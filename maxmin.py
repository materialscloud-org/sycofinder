#! /usr/bin/env python

##################################
# this program generates a diverse set of individuals for initializing GA.
# It uses max-min algorithm to find the most diverse set.
# Easily you can modify it for other needs.
# Mohamad Moosavi 13Dec 2017
##################################

import numpy as np
import itertools
import time


def check_sample(a, var_LB, var_UB):
    # this function check if the randomely generated sample point
    # lies on the phase space. In other words, it applies the constraints.
    # For example, the volume of solvent in our study should not be above 6ml.
    a = np.asarray(a)
    a = np.multiply(a, (var_UB - var_LB)) + var_LB
    vol = np.sum(a[0:5])
    cond = vol <= 6 and vol >= 1

    return cond


def compute_distance(x, y, w):
    # This function compute the pairwise distance between two vectors.
    # It weigths the distance based on the importance of variables.
    return np.linalg.norm(w * (x - y))


def min_max(selected_set, nsamples, NPS, var_importance):
    # This function returns the most diverse set of parameters weighted with variable importance.
    selected_indices = []
    if len(selected_set) > nsamples:
        print("Already selected set, no need for minMaX!")
        return selected_set, selected_indices

    if not selected_set:
        selected_set = [np.zeros([1, NPS.shape[1]])]
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
        print(
            np.argmax(distances), distances[np.argmax(distances)],
            " execution time for current landmark: ", extime)
        selected_indices.append(np.argmax(distances))
        selected_set.append(NPS[np.argmax(distances), :])
    print("Total execution time of MaxMin: ", time.time() - prtime_start)
    return selected_set, selected_indices


def compute(var_importance, var_LB, var_UB, num_samples=10, ngrids_per_dim=5):
    """Compute most diverse set of inputs.

    :param var_importance: list of weights
    :param var_LB: list of lower bounds
    :param var_UB: list of upper bounds
    :param num_samples: number of samples to pick
    :param ngrids_per_dim: number of grid points in each variable

    :return result: String containing coordinates of sample points.
    """
    num_variables = len(var_importance)

    grids_dim = np.linspace(
        0,
        1,
        num=ngrids_per_dim,
        endpoint=True,
    )
    print("On each dimension, we sample: ", grids_dim)
    #var_importance  =  np.array([1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0])
    #var_LB  =          np.array(  [ 0.0 ,  0.0  , 0.00 ,  0.00   ,  0.00    ,  0.80     ,  100        , 150   ,   2    ])
    #var_UB  =          np.array(  [ 6.0 ,  6.0  , 6.00 ,  6.00   ,  6.00    ,  1.80     ,  200        , 250   ,   60   ])
    NPS1 = itertools.product(grids_dim, repeat=num_variables)
    #NPS1=[np.array(i) for i in NPS1 if check_sample(i,var_LB,var_UB)]
    NPS1 = [np.array(i) for i in NPS1]
    NPS1 = np.asarray(NPS1)
    print("In total, there are ", len(NPS1), "samples in the space\n")

    norm_diverse_set, sel_ind = min_max([], num_samples, NPS1, var_importance)
    print(NPS1[sel_ind])
    print(norm_diverse_set)
    diverse_set = np.multiply(NPS1[sel_ind], var_UB - var_LB) + var_LB
    #print(diverse_set)

    #result = ""
    #for line in diverse_set:
    #    result += "  ".join("%10.1f"%(round(elem*2)/2) for elem in line[:5])
    #    result += "%10.1f"%(line[5])
    #    result += "  ".join("%10.0f"%(round(elem*2)/2) for elem in line[6:])
    #    result += "\n"

    return diverse_set
