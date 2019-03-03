import matplotlib.pyplot as plt
import numpy as np


fig, ax = plt.subplots()

ax.set_xlim((-5, 5))
ax.set_ylim((-5, 5))
ax.set_aspect("equal")

major_ticks = np.arange(-5, 5, 1)
minor_ticks = np.arange(-5, 5, .25)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.7)

ax.set_title("Парабола")
ax.set_xlabel("x")
ax.set_ylabel("y")

x = np.linspace(-5, 5, 100)
y = x ** 2

ax.plot(x, y, 'b')

plt.show()
