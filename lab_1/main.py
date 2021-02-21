import sys

# load data from file
filename = sys.argv[1]
X, Y, Y_P = [], dict(), dict()
for line in open(filename, "rt").readlines():
    nums = [float(num) for num in line.split()]
    X.append(nums[0])
    Y[nums[0]], Y_P[nums[0]] = nums[1:]

def fill_high_order_diffs(diffs, X, n):
    for order in range(1, n):
        for i in range(n - order):
            xx = tuple(X[i:i + 2 + order])
            diffs[xx] = (diffs[xx[:-1]] - diffs[xx[1:]]) / (xx[0] - xx[-1])

def make_y(X, Y, diffs, n, x):
    y, x_prod = Y[X[0]], x - X[0]
    for i in range(n):
        xx = tuple(X[:i+2])
        y += x_prod * diffs[xx]
        x_prod *= x - X[i+1]
    return y

def newton(X, Y, n, x):
    X = sorted(X, key=lambda xi: abs(x - xi))
    X = sorted(X[:n+1])

    diffs = dict()
    for i in range(n):
        xx = tuple(X[i:i+2])
        diffs[xx] = (Y[xx[0]] - Y[xx[1]]) / (xx[0] - xx[1])

    fill_high_order_diffs(diffs, X, n)
    return make_y(X, Y, diffs, n, x)

def ermit(X, Y, Y_P, n, x):
    X = sorted(X, key=lambda xi: abs(x - xi))
    X = sorted(X[:(n+2)//2] * 2)

    diffs = dict()
    for i in range(n):
        xx = tuple(X[i:i+2])
        if X[i] == X[i+1]:
            diffs[xx] = Y_P[xx[0]]
        else:
            diffs[xx] = (Y[xx[0]] - Y[xx[1]]) / (xx[0] - xx[1])

    fill_high_order_diffs(diffs, X, n)
    return make_y(X, Y, diffs, n, x)

x = 0.525
print(f"x = {x}")
print("  n  |   y (newton)  |  y (ermit)  ")
print("=====|===============|=============")
for n in range(0, 5):
    y_n = newton(X, Y, n, x)
    y_e = ermit(X, Y, Y_P, n, x)
    print(f"  {n}  |    {y_n:.5g}    |   {y_e:.5g}")
