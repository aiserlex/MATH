from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad


def cos2(x):
    return np.cos(x**2)


def sin2(x):
    return np.sin(x**2)


param = np.linspace(-6, 6, 601)

x = [quad(cos2, 0, val)[0] for val in param]
y = [quad(sin2, 0, val)[0] for val in param]

X = x - 0.5 * sin2(param) / param
Y = y + 0.5 * cos2(param) / param

fig, ax = plt.subplots()
ax.axis('equal')
ax.axhline(y=0, color='k', lw=1)
ax.axvline(x=0, color='k', lw=1)
ax.set_xlim((-1, 1))
ax.set_ylim((-1, 1))
ax.grid()

ax.plot(x, y, lw=0.8, label='1')
ax.plot(X, Y, lw=0.8, label='2')
dot = ax.plot([], [], 'r.')[0]
# radi = ax.plot([], [], 'r.')[0]

circ = Circle((X[100], Y[100]), radius=0.5/param[100],
              color='red', lw=1,fill=False)
ax.add_patch(circ)

plt.legend(loc='upper left')

def update(index):
    circ.center = (X[index], Y[index])
    circ.set_radius(0.5 / param[index])
    dot.set_data(X[index], Y[index])
    # radi.set_data(x[index], y[index])
    return circ, dot#, radi

anim = FuncAnimation(fig, update, frames=range(0, len(param), 2),
                     interval=20, blit=True)
# anim.save('line2.gif', writer='imagemagick')

plt.show()
