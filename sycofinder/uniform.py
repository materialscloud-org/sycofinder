"""
Uniform sampling using pymc
"""

# pylint: skip-file

# Note: in pymc you can easily add constraints:
# https://healthyalgorithms.com/2008/11/05/mcmc-in-python-pymc-to-sample-uniformly-from-a-convex-body/


def compute(var_LB, var_UB, num_samples=10):
    from pymc import Uniform, MCMC

    X = Uniform('X', var_LB, var_UB)
    mc = MCMC([X])
    mc.sample(num_samples)

    #import matplotlib.pyplot as plt
    #plt.plot(X.trace()[:,0], X.trace()[:,1],',')
    #plt.show()

    return X.trace()
