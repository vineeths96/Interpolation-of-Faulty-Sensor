from parameters import *


def kalman_filter(y_n, sigma_v, sigma_w, x_n1_n1, P_n1_n1):
    """
    Kalman filter implementation
    :param y_n: Observation at n
    :param sigma_v: Std deviation for v(n)
    :param sigma_w: Std deviation for w(n)
    :param x_n1_n1: True signal at n-1
    :param P_n1_n1: True error at n-1
    :return: True and estimated signal, true and predicted error
    """

    x_n_n1 = alpha * x_n1_n1
    P_n_n1 = (alpha ** 2) * P_n1_n1 + (sigma_w ** 2)
    K = P_n_n1 * ((sigma_v ** 2 + P_n_n1) ** -1)

    x_n_n = x_n_n1 + K * (y_n - x_n_n1)
    P_n_n = (1 - K) * P_n_n1

    return x_n_n, x_n_n1, P_n_n, P_n_n1
