import sys

# загрузка данных из файла
filename = sys.argv[1]
X, Y, Z = [], [], {}
with open(filename, "rt") as file:
    X = list(map(float, file.readline().split()[1:]))
    for line in file:
        y, *vals = list(map(float, line.split()))
        Y.append(y)
        for x, val in zip(X, vals):
            Z[(x, y)] = val

# линейный сплайн
def calc_lin_spline_data(X, Y):
    A = Y[:-1]
    B = [(Y[i] - Y[i - 1]) / (X[i] - X[i - 1]) for i in range(1, len(X))]

    return A, B

# квадратичный сплайн
def calc_quad_spline_data(X, Y, slope0=0):
    n = len(X)

    A = Y[:-1]
    B, C = [0] * (n - 1), [0] * (n - 1)

    B[0] = slope0
    C[0] = ((Y[1] - Y[0]) / (X[1] - X[0]) - B[0]) / (X[1] - X[0])
    for i in range(1, n - 1):
        B[i] = B[i - 1] + 2 * C[i - 1] * (X[i] - X[i - 1])
        C[i] = ((Y[i + 1] - Y[i]) / (X[i + 1] - X[i]) - B[i]) / (X[i + 1] - X[i])

    return A, B, C

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

# интерполяция по табличной функции одной
# переменной с заданной степенью полиномов
def interpolate(X, Y, x, n):
    if   n == 1: data = calc_lin_spline_data(X, Y)
    elif n == 2: data = calc_quad_spline_data(X, Y)
    elif n == 3: data = calc_qubic_spline_data(X, Y)
    else: raise RuntimeError("invalid param 'n'. Must be 1, 2 or 3")

    return apply_interp_data(X, data, x)

# интерполирования исходной табличной функции
# двух переменных с заданными степенями полиномов
def z_func(x, y, n_x, n_y):
    ZX = [interpolate(X, [Z[(xi, yi)] for yi in Y], x, n_x) for xi in X]
    return interpolate(Y, ZX, y, n_y)

# начальные параметры интерполирования
x, y = 1.5, 1.5

print(" n |  x  |  y  | z real | z interp ")
print("===|=====|=====|========|==========")
for n in [1, 2, 3]:
    z = z_func(x, y, n, n)
    print(f" {n} | {x} | {y} | {x ** 2 + y ** 2:.4f} | {z:.6f}")

# вывод графика интерполированной функции
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def test_1d():
    X = [0, 1, 2, 3, 4, 5]
    Y = [0, 1, 9, 2, 16, 10]

    X_ext = np.linspace(min(X), max(X), 100)

    Y_interp = [interpolate(X, Y, x, 1) for x in X_ext]
    plt.plot(X_ext, Y_interp, 'r-', label="линейный сплайн")

    Y_interp = [interpolate(X, Y, x, 2) for x in X_ext]
    plt.plot(X_ext, Y_interp, 'g-', label="квадратичный сплайн")

    Y_interp = [interpolate(X, Y, x, 3) for x in X_ext]
    plt.plot(X_ext, Y_interp, 'y-', label="кубический сплайн")

    plt.plot(X, Y, 'bo')
    plt.legend()
    plt.show()

def test_2d():
    num = 100
    xx = np.linspace(X[0], X[-1], num)
    yy = np.linspace(Y[0], Y[-1], num)

    XX, YY = np.meshgrid(xx, yy)
    ZZ = np.zeros(XX.shape)

    for i, x in enumerate(xx):
        for j, y in enumerate(yy):
            ZZ[i, j] = z_func(x, y, 3, 3)

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(XX, YY, ZZ)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

test_1d()
test_2d()
