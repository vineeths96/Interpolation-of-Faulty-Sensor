import numpy as np
import matplotlib.pyplot as plt
from kalman_filter import kalman_filter
from paramaters import *


def generate_obs_seq():
    x = np.zeros(N)

    variance_x = sigma_w ** 2 / (1 - alpha ** 2)
    sigma_x = np.sqrt(variance_x)
    x_0 = sigma_x * np.random.randn(1)

    x[0] = x_0
    for n in range(1, N):
        w = sigma_w * np.random.randn(1)
        x[n] = alpha * x[n - 1] + w

    return x


def main():
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

    plt.figure()
    plt.plot(x_true, label="True x[n]")
    plt.plot(x_pred, label="Estimated x[n]")
    plt.xlabel("n")
    plt.ylabel("x[n]")
    plt.title("True and Estimated signal")
    plt.legend()
    plt.savefig('./results/Kalman_1.png')

    plt.figure()
    plt.plot(P_true, label="True Error")
    plt.plot(P_pred, label="Estimated Error")
    plt.xlabel("n")
    plt.ylabel("Error")
    plt.title("True and Predicted error")
    plt.legend()
    plt.savefig('./results/Kalman_2.png')


if __name__ == '__main__':
    main()
