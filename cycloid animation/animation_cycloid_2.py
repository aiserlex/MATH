import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def update(frame):
    circ.set_center((frame / 10, 1))
    x0 = 0
    y0 = 1
    x1 = -np.cos(frame / 10 - np.pi/2)
    y1 = np.sin(frame / 10 - np.pi/2)
    line.set_data([x0 + frame / 10, x1 + frame / 10], [y0, y1+1])
    return circ, line

fig = plt.figure()
ax = fig.add_subplot(111, xlim=(-1, 15), ylim=(-1, 3))
ax.set_aspect('equal')
# ax.grid()
t = np.linspace(0, 50, 1000)
m = t - np.sin(t)
n = 1 - np.cos(t)
ax.plot(m, n, 'r')

circ = ax.add_artist(plt.Circle((0, 1), 1))
line, = ax.plot([], [], 'w')

anim = FuncAnimation(fig, update, interval=10, frames=165)

plt.show()
