from numpy import array
from numpy.linalg import inv

from gui import App


def best_sqr_approx(X: list, Y: list, W: list, n: int):
    n += 1
    N = len(X)

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


App().feed_approximator(best_sqr_approx).mainloop()
