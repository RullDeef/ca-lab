from typing import Callable as func


def simpson_integrate(f: func, a: float, b: float, n: int) -> float:
    h, res = (b - a) / n, 0
    for i in range(0, n, 2):
        x1, x2, x3 = i * h, (i + 1) * h, (i + 2) * h
        f1, f2, f3 = f(x1), f(x2), f(x3)
        res += f1 + 4 * f2 + f3
    return h / 3 * res


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from numpy import linspace

    def test_f(x):
        return 0.3 * (x - 1)**2 - 0.1 * (x + 4)**2 - x

    def act_int_f(x):
        return 0.1 * (x - 1)**3 - 0.1 / 3 * (x + 4)**3 - 0.5 * x**2

    X = linspace(-10, 10, 100)
    Y = act_int_f(X) - act_int_f(0 * X)
    F = lambda n: [simpson_integrate(test_f, 0, x, n) for x in X]

    plt.plot(X, Y)
    plt.plot(X, F(4))
    plt.show()
