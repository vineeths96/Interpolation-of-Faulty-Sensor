from paramaters import *


def kalman_filter(y_n, sigma_v, sigma_w, x_n1_n1, P_n1_n1):
    x_n_n1 = alpha * x_n1_n1
    P_n_n1 = (alpha ** 2) * P_n1_n1 + (sigma_w ** 2)
    K = P_n_n1 * ((sigma_v ** 2 + P_n_n1) ** -1)

    x_n_n = x_n_n1 + K * (y_n - x_n_n1)
    P_n_n = (1 - K) * P_n_n1

    return x_n_n, x_n_n1, P_n_n, P_n_n1
