from numpy import linspace, array
from numpy.linalg import solve
from typing import Callable as func
from typing import List


# Возвращает значение полинома Лежандра n-го порядка
def legendre(n: int, x: float) -> float:
    if n < 2: return [1, x][n]
    P1, P2 = legendre(n - 1, x), legendre(n - 2, x)
    return ((2 * n - 1) * x * P1 - (n - 1) * P2) / n


# Нахождение корней полинома Лежандра n-го порядка
def legendre_roots(n: int, eps: float = 1e-12) -> List[float]:
    roots = [0] * n
    sections = linspace(-1, 1, n + 1)
    sections = zip(sections[:-1], sections[1:])
    for i, (a, b) in enumerate(sections):  # уточнение корней
        root = (a + b) / 2
        root_val = legendre(n, root)
        a_val = legendre(n, a)
        while abs(root_val) > eps:
            if a_val * root_val < 0: b = root
            else: a, a_val = root, root_val
            root = (a + b) / 2
            root_val = legendre(n, root)
        roots[i] = root
    return roots


# Метод Гаусса для численного интегрирования на [-1; 1]
def gauss_integrate_norm(f: func, n: int) -> float:
    t = legendre_roots(n)
    T = array([[t_i**k for t_i in t] for k in range(n)])

    int_tk = lambda k: 2 / (k + 1) if k % 2 == 0 else 0
    b = array([int_tk(k) for k in range(n)])
    A = solve(T, b)  # решение системы линейных уравнений

    return sum(A_i * f(t_i) for A_i, t_i in zip(A, t))


# Метод Гаусса для произвольного промежутка [a; b]
def gauss_integrate(f: func, a: float, b: float, n: int) -> float:
    mean, diff = (a + b) / 2, (b - a) / 2
    g = lambda t: f(mean + diff * t)
    return diff * gauss_integrate_norm(g, n)


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    def test_f(x):
        return 0.3 * (x - 1) ** 2 - 0.1 * (x + 4) ** 2 - x

    def act_int_f(x):
        return 0.1 * (x - 1) ** 3 - 0.1 / 3 * (x + 4) ** 3 - 0.5 * x ** 2

    X = linspace(-10, 10, 100)
    Y = act_int_f(X) - act_int_f(0 * X)
    F = lambda n: [gauss_integrate(test_f, 0, x, n) for x in X]

    plt.plot(X, Y)
    plt.plot(X, F(1))
    plt.show()
