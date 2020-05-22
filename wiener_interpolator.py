import numpy as np
from parameters import *


def wiener_interpolator1(x, n_0, alpha):
    """
    Wiener interpolator using all observations
    :param x: Observation vector except at n_0
    :param n_0: The time instant of interpolation
    :param alpha: Value of alpha
    :return: The predicted value at n_0 and BMSE
    """

    R = np.zeros([N - 1, N - 1])
    r = np.zeros(N - 1)
    a = np.zeros(N - 1)

    for i in range(N - 1):
        for j in range(N - 1):
            if np.abs(i - j) < n_0:
                R[i, j] = alpha ** np.abs(i - j)
            else:
                R[i, j] = alpha ** np.abs(i - j + 1)

    for i in range(N - 1):
        if i < n_0:
            r[i] = alpha ** (n_0 - i)
        else:
            r[i] = alpha ** (i - n_0 + 1)

    R_inv = np.linalg.inv(R)
    a = R_inv @ r
    x_n_0 = np.dot(a, x)

    r_0 = sigma_w ** 2 / (1 - alpha ** 2)
    BMSE = r_0 - np.transpose(r) @ R_inv @ r

    return x_n_0, BMSE


def wiener_interpolator2(x, n_0, alpha):
    """
    Wiener interpolator using observations x[n_0 - 1] and x[n_0 + 1]
    :param x: Observation vector except at n_0
    :param n_0: The time instant of interpolation
    :param alpha: Value of alpha
    :return: The predicted value at n_0 and BMSE
    """

    x_n_0 = alpha / (1 + alpha ** 2) * (x[n_0 - 1] + x[n_0 + 1])

    r_0 = sigma_w ** 2 / (1 - alpha ** 2)
    r_1 = alpha * r_0
    r_2 = alpha * r_1

    r = np.array([r_1, r_1])
    R = np.array([[r_0, r_2], [r_2, r_0]])
    R_inv = np.linalg.inv(R)

    BMSE = r_0 - np.transpose(r) @ R_inv @ r

    return x_n_0, BMSE
