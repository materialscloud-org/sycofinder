from ga import main as ga_main
import numpy as np
import unittest


def rastrigin_func(X):
    X = X - np.array([5.12, 5.12])
    s = np.power(X, 2) - 10 * np.cos(2 * np.pi * X)
    return -1 * (10 * len(X) + sum(s))


def gaussians(X):
    sigma = 1
    mu1 = [4, 4]
    h1 = 3
    s = h1 * np.exp(-0.5 * (np.sqrt((X[0] - mu1[0])**2 +
                                    (X[1] - mu1[1])**2) / sigma)**2)
    mu2 = [2, 2]
    h2 = 1
    s += h2 * np.exp(-0.5 * (np.sqrt((X[0] - mu2[0])**2 +
                                     (X[1] - mu2[1])**2) / sigma)**2)
    return s


class GATestCase(unittest.TestCase):
    def test_gaussians(self):
        """Test that minimum between two Gaussians is found correctly"""
        inputs = np.random.rand(30, 2) * 10  # 5x5 domain
        fitn = np.apply_along_axis(gaussians, 1,
                                   inputs[:]).reshape([inputs.shape[0], 1])
        inigen = np.hstack([inputs, fitn])
        names = ["var1", "var2", "fitness"]
        for gen in range(100):
            if gen == 0:
                oldgen = inigen
            new_pop, _var = ga_main(oldgen, names, 1)
            fitn = np.apply_along_axis(gaussians, 1, new_pop[:]).reshape(
                [new_pop.shape[0], 1])
            oldgen = np.hstack([new_pop, fitn])
        optimal_computed = np.amax(fitn)
        optimal_theory = gaussians([4, 4])

        self.assertAlmostEqual(optimal_computed, optimal_theory, delta=0.1)

    def test_rastrigin(self):
        """Test that minimum of rastrigin function is found correctly
        
        See https://en.wikipedia.org/wiki/Rastrigin_function
        """
        inputs = np.random.rand(30, 2) * 10.24
        fitn = np.apply_along_axis(rastrigin_func, 1,
                                   inputs[:]).reshape([inputs.shape[0], 1])
        inigen = np.hstack([inputs, fitn])
        names = ["var1", "var2", "fitness"]
        for gen in range(100):
            if gen == 0:
                oldgen = inigen
            new_pop, _var = ga_main(oldgen, names, 1)
            fitn = np.apply_along_axis(rastrigin_func, 1, new_pop[:]).reshape(
                [new_pop.shape[0], 1])
            oldgen = np.hstack([new_pop, fitn])
        optimal_computed = np.amax(fitn)
        optimal_theory = rastrigin_func(np.array([5.12, 5.12]))

        self.assertAlmostEqual(optimal_computed, optimal_theory, delta=3.0)
