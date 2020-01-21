import cvxpy as cvx
import numpy as np
import dccp  # pylint: disable=unused-import

np.random.seed(0)


def max_min_dccp(n_samples, var_importance):
    """Solve MaxMin Diversity problem on hypercube

    :nsamples : number of samples 
    :var_importance:  list of floats, specifying importance of each variable
    """
    radii = np.ones(n_samples)  # radii
    v_scale = cvx.vec(var_importance)

    c = cvx.Variable((n_samples, len(var_importance)))
    constr = []
    for i in range(n_samples - 1):
        for j in range(i + 1, n_samples):
            # distance vector is scaled by variable importance
            d = cvx.multiply(cvx.vec(c[i, :] - c[j, :]), v_scale)
            constr.append(cvx.norm(d, 2) >= radii[i] + radii[j])

    # minimize the size of the square to fit the given spheres
    # (by minimzing the largest component of any center vector)
    prob = cvx.Problem(
        cvx.Minimize(cvx.max(cvx.max(cvx.abs(c), axis=1) + radii)), constr)
    prob.solve(method='dccp', solver='ECOS', ep=1e-2, max_slack=1e-2)

    l = cvx.max(cvx.max(cvx.abs(c), axis=1) + radii).value * 2
    pi = np.pi
    ratio = pi * cvx.sum(cvx.square(radii)).value / cvx.square(l).value
    print("ratio =", ratio)

    # shift to positive numbers
    coords = c.value - np.min(c.value)
    # scale maximum coordinate to 1
    coords /= np.max(coords)

    return coords
