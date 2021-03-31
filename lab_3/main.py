from numpy import linspace

# исходные данные
N = 4
X = linspace(0, 10, N)
Y = X ** 2

# интерполяция полиномом Ньютона
def newton(X, Y, n, x):
    def fill_high_order_diffs(diffs, X, n):
        for order in range(1, n):
            for i in range(n - order):
                xx = tuple(X[i:i + 2 + order])
                diffs[xx] = (diffs[xx[:-1]] - diffs[xx[1:]]) / (xx[0] - xx[-1])

    def make_y(X, Y, diffs, n, x):
        y, x_prod = Y[X[0]], x - X[0]
        for i in range(n):
            xx = tuple(X[:i + 2])
            y += x_prod * diffs[xx]
            x_prod *= x - X[i + 1]
        return y

    Y = dict(zip(X, Y))
    X = sorted(X, key=lambda xi: abs(x - xi))
    X = sorted(X[:n + 1])

    diffs = dict()
    for i in range(n):
        diffs[tuple(X[i:i + 2])] = (Y[X[i]] - Y[X[i + 1]]) / (X[i] - X[i + 1])

    fill_high_order_diffs(diffs, X, n)
    return make_y(X, Y, diffs, n, x)

# кубический сплайн
def calc_qubic_spline_data(X, Y):
    n = len(X)
    A = Y[:-1]

    ksi, eta = [0, 0], [0, 0]
    for i in range(2, n): # прямой проход
        hi, him1 = X[i] - X[i - 1], X[i - 1] - X[i - 2]
        fi = 3 * ((Y[i] - Y[i - 1]) / hi - (Y[i - 1] - Y[i - 2]) / him1)
        ksi.append(- hi / (him1 * ksi[i - 1] + 2 * (him1 + hi)))
        eta.append((fi - him1 * eta[i - 1]) / (him1 * ksi[i - 1] + 2 * (him1 + hi)))

    C = [0] * (n - 1)
    C[n - 2] = eta[-1]
    for i in range(n - 2, 0, -1): # обратный проход
        C[i - 1] = ksi[i] * C[i] + eta[i]

    B, D = [], []
    for i in range(1, n - 1):
        hi = X[i] - X[i - 1]
        B.append((Y[i] - Y[i - 1]) / hi - hi / 3 * (C[i] + 2 * C[i - 1]))
        D.append((C[i] - C[i - 1]) / 3 / hi)
    B.append((Y[-1] - Y[-2]) / (X[-1] - X[-2]) - (X[-1] - X[-2]) / 3 * 2 * C[-1])
    D.append(- C[n - 2] / 3 / (X[-1] - X[-2]))

    return A, B, C, D

# использование коэф.-тов интерполяции для нахождения
# интерполированного значения табличной функции
def apply_interp_data(X, data, x):
    i = max([0] + list(filter(lambda i: X[i] < x, range(len(X)))))
    y, h = 0, x - X[i]
    for k, row in enumerate(data):
        y += row[i] * h ** k
    return y

x1, x2 = 0.5, 5.5           # точки интерполирования
y1, y2 = x1 ** 2, x2 ** 2   # актуальные значения

# коэффициенты интерполяции
data = calc_qubic_spline_data(X, Y)

# интерполированные значения
y1_i = apply_interp_data(X, data, x1)
y2_i = apply_interp_data(X, data, x2)

print("  x  |   y   |  y интерп.  ")
print("=====|=======|=============")
print(f" {x1} | {y1:5.2f} | {y1_i:7.2f}")
print(f" {x2} | {y2:5.2f} | {y2_i:7.2f}")

# вывод графика интерполированной функции
from matplotlib import pyplot as plt

X_ext = linspace(min(X), max(X), 100)
Y_ext = X_ext ** 2
Y_newton = [newton(X, Y, 3, x) for x in X_ext]
Y_interp = [apply_interp_data(X, data, x) for x in X_ext]

plt.plot(X_ext, Y_ext, 'g--', label="y(x) = x^2")
plt.plot(X_ext, Y_newton, 'r-.', label="Ньютон 3 степени")
plt.plot(X_ext, Y_interp, 'y-', label="кубический сплайн")

plt.plot(X, Y, 'bo')
plt.legend()
plt.show()
