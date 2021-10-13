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
import dask_distance


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


def maxmin(nsamples, NPS, var_importance):  # pylint: disable=unused-argument
    # This function returns the most diverse set of parameters weighted with variable importance.
    selected_indices = []
    selected_set = []
    if len(selected_set) > nsamples:
        print("Already selected set, no need for minMaX!")
        return selected_set, selected_indices

    if len(selected_set) == 0:
        selected_set = [NPS[0, :]]
        selected_indices.append(0)

    prtime_start = time.time()
    test_time = [time.time()]
    while len(selected_set) < nsamples:
        # selected_set_array = np.array(selected_set)
        last_entry = selected_set[-1].reshape(1, -1)
        dtemp = dask_distance.cdist(last_entry, NPS, metric='euclidean')
        d = np.asarray(dtemp)
        if len(selected_set) > 1:
            dmat = np.vstack([dmat, d])
        else:
            dmat = d
        new_ind = np.argmax(np.amin(dmat, axis=0))
        print(new_ind)
        selected_indices.append(new_ind)
        selected_set.append(NPS[new_ind, :])
        if len(selected_set) % 10 == 0:
            print("\n\n found landmark %i out of %i" %
                  (len(selected_set), nsamples))
            print("size of the space is :", np.amax(dmat),
                  " and size of the Voronoi cell is: ",
                  np.amax(np.amin(dmat, axis=0)))
            test_time.append(time.time())
            print("CPU clock time to find the past 10 landmarks:",
                  test_time[-1] - test_time[-2])
    print(("Total execution time of MaxMin: ", time.time() - prtime_start))
    return selected_set, selected_indices


# pylint: disable=too-many-arguments
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
        NPS1 = np.stack(
            np.meshgrid(*itertools.repeat(grids_dim, num_variables)),
            -1).reshape(-1, num_variables)
        print(("In total, there are ", len(NPS1), "samples in the space\n"))

        norm_diverse_set, sel_ind = maxmin(num_samples, NPS1, var_importance)
        print(norm_diverse_set)
        coords = NPS1[sel_ind]

    elif method == 'convex-opt':
        from .maxmin_dccp import max_min_dccp  # pylint: disable=import-outside-toplevel
        coords = max_min_dccp(num_samples, var_importance)

    else:
        raise ValueError("Unknown method {}".format(method))

    diverse_set = np.multiply(coords, var_UB - var_LB) + var_LB

    return diverse_set
