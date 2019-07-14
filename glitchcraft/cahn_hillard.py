# Cahn-Hilliard integrator ported from MATLAB (https://www.math.utah.edu/~eyre/computing/matlab-intro/ch.txt)
# Solves the CH equation with natural and no-flux boundary conditions. Nonlinear term: f(u) = u - u**3
# self-contained integration method means not having to pull in any FEA libraries
# Numerical scheme: Eyre's linearly stabilized CH integration scheme
#
# Notes;:
#  1. Uses a fixed time step.
#  2. Uses discrete cosine transform to invert the linear update matrix by performing a spectral decomposition of the matrix.    
#  3. Calculates spinodal decomposition from random initial conditions with mean value close to zero.
#  4. With the given parameters, there are roughly 10 grid points in a transition layer.    
#  5. The timestep probably should be shorter initially and lengthed later for a more accurate solution.    

from math import pi

import matplotlib.pyplot as plt
import numpy as np
import scipy
from numpy import cos, linspace, ones
from numpy.random import rand
from PIL import Image
from scipy.fftpack import dct, idct

from glitchcraft.utils import progress


# two-dimensional discrete cosine transform
def dct2(a):
    return dct(dct(a, axis=0, norm="ortho"), axis=1, norm="ortho")


def idct2(a):
    return idct(idct(a, axis=0, norm="ortho"), axis=1, norm="ortho")

def update(U, U_hat, a, S_eig, CH_eig):
    """ run a simulation step and return the next state """
    # compute the shifted nonlinear term
    fU = (U * U * U) - ((1 + a) * U)

    # compute the updated solution in tranform space
    U_hat = (U_hat + (S_eig * dct2(fU))) / CH_eig

    # invert the cosine transform
    return idct2(U_hat), U_hat

def integrate(src, dt = 0.00005, epsilon = 0.01, a =2):
    """ runs cahn-hillard simulation 
    
    src: should be a square, black and white or single channel image

    dt: time step between states, (should really be exponentially growing)

    epsilon**2: the coefficient of the Laplacian term in the CH equation. 
    to see more layering, decrease epsilon, but be careful, you might need to increase
    the size of the grid.

    a: is the time step parameter used in Eyre's method

    """
    (N, M) = src.size
    assert N == M, "discrete cosine transform requires square image"

    # set up initial conditions
    # CH parameters 
    dx2 = (1 / (M - 1)) ** 2
    eps2 = epsilon ** 2

    # time marching update parameters
    lambda_1 = dt / dx2
    lambda_2 = eps2 * lambda_1 / dx2

    # unscaled eigenvalues of the Laplacian (Neumann boundary counditions)
    L_eig = \
        (((2 * cos(pi * np.arange(N) / (N - 1))) - 2) * ones((1, M))) +\
        (ones((N, 1)) * ((2 * cos(pi * np.arange(M) / (M - 1))) - 2))

    # scaled eigenvalues of stabilized CH update matrix
    CH_eig = ones((N, M)) - (a * lambda_1 * L_eig) + (lambda_2 * L_eig * L_eig)

    # scaled eigenvalues of the Laplacian
    S_eig = lambda_1 * L_eig

    U = np.asarray(src)/256
    U_hat = dct2(U)

    yield (256 * U).astype(int)

    # main loop
    while True:
        U, U_hat  = update(U, U_hat, a, S_eig, CH_eig)
        yield (256 * U).astype(int)