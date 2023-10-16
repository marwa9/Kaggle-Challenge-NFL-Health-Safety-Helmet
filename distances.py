# -*- coding: utf-8 -*-

from scipy.stats import wasserstein_distance
from scipy.spatial import distance
from fastdtw import fastdtw
import numpy as np


# Hausdorff Distance
def Hausdorff_distance(curve1, curve2):
    distance_matrix = distance.cdist(curve1, curve2)
    max_dist_curve1 = np.max(np.min(distance_matrix, axis=1))
    max_dist_curve2 = np.max(np.min(distance_matrix, axis=0))
    return max(max_dist_curve1, max_dist_curve2)

# Wasserstein Distance
def Wasserstein(x_coordinates1, y_coordinates1,x_coordinates2, y_coordinates2):
    emd_x = wasserstein_distance(x_coordinates1, x_coordinates2)
    emd_y = wasserstein_distance(y_coordinates1, y_coordinates2)
    similarity = 1 / (1 + emd_x + emd_y)
    return similarity

# Fastdtw Distance
def Fastdtw_distance(curve1, curve2):
    fastdtw_distance_result, _ = fastdtw(curve1, curve2)
    return fastdtw_distance_result

# Fréchet Distance
def Euclidean_distance(p1, p2):
    return distance.euclidean(p1, p2)

def Discrete_frechet(curve1, curve2):
    n = len(curve1)
    m = len(curve2)
    if n == 0 or m == 0:
        raise ValueError("Input curves cannot be empty")
    
    def c(i, j):
        return Euclidean_distance(curve1[i], curve2[j])

    ca = -np.ones((n, m))
    
    def cA(i, j):
        if ca[i, j] > -1:
            return ca[i, j]
        if i == 0 and j == 0:
            ca[i, j] = c(0, 0)
        elif i > 0 and j == 0:
            ca[i, j] = max(cA(i-1, 0), c(i, 0))
        elif i == 0 and j > 0:
            ca[i, j] = max(cA(0, j-1), c(0, j))
        elif i > 0 and j > 0:
            ca[i, j] = max(min(cA(i-1, j), cA(i-1, j-1), cA(i, j-1)), c(i, j))
        return ca[i, j]
    
    return cA(n-1, m-1)