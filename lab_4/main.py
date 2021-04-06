from numpy import array
from numpy.linalg import inv

from gui import App


def best_sqr_approx(X: list, Y: list, W: list, n: int):
    N = len(X)
    n += 1
    if n >= N:
        n = N

    Y_hat = array([[
        sum(W[k] * Y[k] * X[k] ** i for k in range(N))
        for i in range(n)
    ]])

    mat = [[sum(W[k] * X[k] ** (i + j) for k in range(N))
            for j in range(n)
        ] for i in range(n)
    ]

    mat = inv(mat)
    A = Y_hat.dot(mat).flatten()

    def functor(x):
        y = 0
        for i, a in enumerate(A):
            y += a * x ** i
        return y

    return functor

# Q6
def best_sqr_approx_nm(X: list, Y: list, W: list, n: int):
    def make_functor(A: list):
        def functor(x):
            y = 0
            for i, a in enumerate(A):
                y += a * x ** i
            return y
        return functor

    def error(functor):
        err = 0
        for x, y, w in zip(X, Y, W):
            err += w * (y - functor(x))**2
        return err

    N = len(X)
    err_list = []

    max_power = 10
    for n in range(2, max_power):
        for m in range(1, n):
            Y_hat = array([[
                sum(W[k] * Y[k] * X[k] ** i for k in range(N))
                for i in (0, n, m)
            ]])

            mat = [[sum(W[k] * X[k] ** (i + j) for k in range(N))
                    for j in (0, n, m)
                ] for i in (0, n, m)
            ]

            mat = inv(mat)
            errA = Y_hat.dot(mat).flatten()

            A = [0] * (1 + max(n, m))
            A[0], A[n], A[m] = errA

            err = error(make_functor(A))
            err_list.append((err, n, m, A))

    best_err = sorted(err_list, key=lambda e: e[0])[0]
    err, n, m, A = best_err
    print(n, m)
    return make_functor(A)

App().feed_approximator(best_sqr_approx).mainloop()
