from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from function import function
from numpy import linspace, array, zeros,  arange, meshgrid


n_min, m_min = 3, 4
n_max, m_max = 7, 12
N_ = arange(n_min, n_max + 1)
M_ = arange(m_min, m_max + 1, 2)

X = linspace(0.05, 10, 100)
Y_ideal = array([function(x, n_max, m_max) for x in X])

N, M = meshgrid(N_, M_)
Z = zeros(N.shape, float)

for i, n in enumerate(N_):
    for j, m in enumerate(M_):
        #n, m = N[0, j], M[i, 0]
        Y = array([function(x, n, m) for x in X])
        Z[i, j] = 1000 * ((Y - Y_ideal) ** 2).cumsum()[-1]
        print("done for", n, m, Z[i, j])

print(Z)

fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(N, M, Z)
plt.xlabel('n')
plt.ylabel('m')
plt.show()
