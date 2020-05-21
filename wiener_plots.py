import numpy as np
import matplotlib.pyplot as plt
from wiener_interpolator import wiener_interpolator1, wiener_interpolator2
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
    alpha_list = np.arange(0.1, 1, 0.1)

    TMSE_1 = np.zeros(len(alpha_list))
    TMSE_2 = np.zeros(len(alpha_list))
    BMSE_1 = np.zeros(len(alpha_list))
    BMSE_2 = np.zeros(len(alpha_list))

    for ind, alpha in enumerate(alpha_list):
        TMSE_1_ALPHA = np.zeros(NUM_REALIZATIONS)
        TMSE_2_ALPHA = np.zeros(NUM_REALIZATIONS)
        BMSE_1_ALPHA = np.zeros(NUM_REALIZATIONS)
        BMSE_2_ALPHA = np.zeros(NUM_REALIZATIONS)

        for i in range(NUM_REALIZATIONS):
            x = generate_obs_seq()
            x_n0 = x[n0]
            x = np.delete(x, n0)

            x_n0_pred_1, BMSE_1_ALPHA[i] = wiener_interpolator1(x, n0, alpha)
            x_n0_pred_2, BMSE_2_ALPHA[i] = wiener_interpolator2(x, n0, alpha)

            TMSE_1_ALPHA[i] = (x_n0 - x_n0_pred_1) ** 2
            TMSE_2_ALPHA[i] = (x_n0 - x_n0_pred_2) ** 2

        BMSE_1[ind] = np.sum(BMSE_1_ALPHA) / NUM_REALIZATIONS
        BMSE_2[ind] = np.sum(BMSE_2_ALPHA) / NUM_REALIZATIONS
        TMSE_1[ind] = np.sum(TMSE_1_ALPHA) / NUM_REALIZATIONS
        TMSE_2[ind] = np.sum(TMSE_2_ALPHA) / NUM_REALIZATIONS

        plt.figure()
        plt.plot(alpha_list, BMSE_1, label="BMSE")
        plt.plot(alpha_list, TMSE_1, label="TMSE")
        plt.xlabel("Alpha")
        plt.ylabel("MSE")
        plt.title("Wiener interpolator 1")
        plt.legend()
        plt.savefig('./results/Wiener_1.png')

        plt.figure()
        plt.plot(alpha_list, BMSE_2, label="BMSE")
        plt.plot(alpha_list, TMSE_2, label="TMSE")
        plt.xlabel("Alpha")
        plt.ylabel("MSE")
        plt.title("Wiener interpolator 2")
        plt.legend()
        plt.savefig('./results/Wiener_2.png')


if __name__ == '__main__':
    main()