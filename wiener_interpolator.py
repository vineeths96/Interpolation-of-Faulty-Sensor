import numpy as np
np.set_printoptions(linewidth=np.inf)

N = 100


def wiener_interpolator1(x, n_0, alpha):
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

    a = np.linalg.inv(R) @ r
    x_n_0 = np.dot(a, x)

    return x_n_0


def wiener_interpolator2(x, n_0, alpha):
    x_n_0 = alpha / (1 + alpha ** 2) * (x[n_0 - 1] + x[n_0 + 1])

    return x_n_0
