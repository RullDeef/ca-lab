from matplotlib import pyplot as plt
from numpy import linspace, arange

from function import function

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

major_ticks = linspace(0, 10, 6)
minor_ticks = linspace(0, 10, 21)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(linspace(0, 1, 6))
ax.set_yticks(linspace(0, 1, 11), minor=True)

# And a corresponding grid
ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='minor', alpha=0.4)
ax.grid(which='major', alpha=0.8)

tao = linspace(0.05, 10, 100)
eps = [function(t, 3, 12) for t in tao]
ax.plot(tao, eps, label="ɛ(τ)")

plt.legend()
plt.xlabel("τ")
plt.ylabel("ɛ").set_rotation(0)
#plt.grid()
plt.show()
