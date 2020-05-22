import numpy as np
from parameters import *


def generate_obs_seq():
    """
    Generates a realization of the WSS observation
    """

    x = np.zeros(N)

    # Initialize x[0]
    variance_x = sigma_w ** 2 / (1 - alpha ** 2)
    sigma_x = np.sqrt(variance_x)
    x_0 = sigma_x * np.random.randn(1)

    # Calculate the remaining observations using equation given
    x[0] = x_0
    for n in range(1, N):
        w = sigma_w * np.random.randn(1)
        x[n] = alpha * x[n - 1] + w

    return x


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


def wiener_causal_interpolator(x, n_0, alpha):
    """
    Causal Wiener filter implementation
    :param x: Observation vector for past time instants (< n_0)
    :param n_0: The time instant of prediction
    :param alpha: Value of alpha
    :return: The predicted value at n_0 and BMSE
    """

    N = x.shape[0]
    R = np.zeros([N, N])
    r = np.zeros(N)
    a = np.zeros(N)

    for i in range(N):
        for j in range(N):
            if np.abs(i - j) < n_0:
                R[i, j] = alpha ** np.abs(i - j)
            else:
                R[i, j] = alpha ** np.abs(i - j + 1)

    for i in range(N):
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


def main():
    """
    Compares and produces the result file
    """

    y = generate_obs_seq()

    x_true = np.zeros(n0)
    x_pred = np.zeros(n0)
    P_true = np.zeros(n0)
    P_pred = np.zeros(n0)

    x_true[0] = y[0]
    x_pred[0] = y[0]
    P_true[0] = 1
    P_pred[0] = 1

    for i in range(1, n0):
        x_true[i], x_pred[i], P_true[i], P_pred[i] = kalman_filter(y[i], sigma_v, sigma_w, x_true[i - 1], P_true[i - 1])

    kalman_error = P_true[-1]
    _, wiener_error = wiener_causal_interpolator(y[:n0], n0, alpha)

    with open('./results/comparison.txt', "w") as file:
        file.write("The prediction error for Kalman filter is {:0.4f}.\n".format(kalman_error))
        file.write("The prediction error for causal Wiener filter is {:0.4f}.\n".format(wiener_error))


if __name__ == '__main__':
    main()
