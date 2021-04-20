h = 1
X = [1, 2, 3, 4, 5, 6]
Y = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412 ]
N = len(X)

def side_diff(n: int) -> float:
    if n + 1 == N:  return (Y[n] - Y[n - 1]) / h
    else:           return (Y[n + 1] - Y[n]) / h

def mid_diff(n: int) -> float:
    if n == 0:      return (-3 * Y[0] + 4 * Y[1] - Y[2]) / (2 * h)
    elif n + 1 < N: return (Y[n + 1] - Y[n - 1]) / (2 * h)
    else:           return (Y[n - 2] - 4 * Y[n - 1] + 3 * Y[n]) / (2 * h)

def runge_diff(n: int) -> float:
    if n + 2 >= N:  return (3 * Y[n] - 4 * Y[n - 1] + Y[n - 2]) / (2 * h)
    else:           return (-Y[n + 2] + 4 * Y[n + 1] - 3 * Y[n]) / (2 * h)

def lin_vars_diff(n: int) -> float:
    if n + 1 < N:   return Y[n] / X[n] * X[n + 1] / Y[n + 1] * (Y[n] - Y[n + 1]) / (X[n] - X[n + 1])
    else:           return Y[n - 1] / X[n - 1] * X[n] / Y[n] * (Y[n - 1] - Y[n]) / (X[n - 1] - X[n])

def diff_2(n: int) -> float:
    if n == 0:      return (Y[2] - 2 * Y[1] + Y[0]) / (h * h)
    elif n + 1 < N: return (Y[n + 1] - 2 * Y[n] + Y[n - 1]) / (h * h)
    else:           return (Y[n] - 2 * Y[n - 1] + Y[n - 2]) / (h * h)

for n in range(N):
    print(f"X = {X[n]:2d}", end=" | ")
    print(f"Y = {Y[n]:.3f}", end=" | ")
    print(f"{side_diff(n):.3f}", end=" | ")
    print(f"{mid_diff(n):.3f}", end=" | ")
    print(f"{runge_diff(n):.3f}", end=" | ")
    print(f"{lin_vars_diff(n):.3f}", end=" | ")
    print(f"{diff_2(n):.3f}", end=" | ")
    print()
