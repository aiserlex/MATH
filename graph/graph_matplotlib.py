import matplotlib.pyplot as plt
import numpy as np

XLIM = (-10, 10)
YLIM = (-2, 7)

fig, ax = plt.subplots()

ax.set_xlim(XLIM)
ax.set_ylim(YLIM)
ax.set_aspect("equal")

major_ticks_x = np.arange(*XLIM, 1)
minor_ticks_x = np.arange(*XLIM, .25)
major_ticks_y = np.arange(*YLIM, 1)
minor_ticks_y = np.arange(*YLIM, .25)

ax.set_xticks(major_ticks_x)
ax.set_xticks(minor_ticks_x, minor=True)
ax.set_yticks(major_ticks_y)
ax.set_yticks(minor_ticks_y, minor=True)

ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.7)

ax.set_title("График")
ax.set_xlabel("x")
ax.set_ylabel("y")

x = np.linspace(*XLIM, 1000)
y = x ** 2

ax.plot(x, y, 'b')

plt.show()
