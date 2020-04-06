import numpy as np
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt

np.random.seed(1)

def growth_rate(x, steps=1):
  return x[steps:]-x[:-steps]

def create_DGP(N, T, alpha, var_eps):
  
    """ we do cool stuff here:

    Args:
    N (int) : number of countries
    T (int) : time dimension

    Returns:
    Y (array)
    Y_growth (array)
    """
  # Function that takes all necessary parameters and returns a simulated dataset [NxT]
  Y=np.random.rand(N, T)
  for i in range(N):
    Y[i, 0]=0
    theta = np.random.uniform(1, alpha, 1)
    for t in range(1, T):
      epsilon = np.random.normal(0, sqrt(var_eps), 1)
      Y[i, t]=theta+Y[i, t-1]+epsilon
  Y_growth = np.vstack([growth_rate(row) for row in Y])
  return Y, Y_growth
