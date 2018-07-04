from pymc import Uniform, MCMC
import numpy as np

# Note: in pymc you can easily add constraints:
# https://healthyalgorithms.com/2008/11/05/mcmc-in-python-pymc-to-sample-uniformly-from-a-convex-body/

def compute(
        var_importance,
        var_LB,
        var_UB,
        num_samples=10):

    nd=len(var_importance)

    X = Uniform('X', var_LB, var_UB)
    #X = Uniform('X', np.zeros(nd), var_importance)
    mc = MCMC([X])
    mc.sample(num_samples)

    return X.trace()
    #import matplotlib.pyplot as plt
    #plt.show()
    #plt.plot(X.trace()[:,0], X.trace()[:,1],',')


