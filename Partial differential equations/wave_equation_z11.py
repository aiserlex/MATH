import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from numpy import pi, sin, cos


a = 1
xlim = (0, 2)
ylim = (-10, 10)
tlim = (0, 20)

x = np.linspace(*xlim, 50)
dx = x[1] - x[0]
X = len(x)

t = np.linspace(*tlim, 1300)
dt = t[1] - t[0]
T = len(t)

assert a**2 * dt**2 / dx**2 < 1, "Нарушено условие устойчивости."

u = np.zeros((T, X))

u[:, 0] = 0
u[:, X - 1] = 0

u[0, :] = 0
u[1, :] = (3*sin(pi*x/2)+6*sin(3*pi*x/2))*dt

for k in range(1, T - 1):
    for j in range(1, X - 1):
        u[k+1, j] = 2*u[k, j] - u[k-1,j]+a**2*dt**2/dx**2*(u[k,j+1]-2*u[k,j]+u[k,j-1])

fig, ax  = plt.subplots()

ax.grid(True)
ax.set_xlim(xlim)
ax.set_ylim(ylim)

line, = ax.plot([], [], 'b')
line_exact, = ax.plot([], [], '.r')
def update(index):
    line.set_data(x, u[index])
    v = 6/pi*sin(pi*t[index]/2)*sin(pi*x/2) +4/pi*sin(3*pi*t[index]/2)*sin(3*pi*x/2)
    line_exact.set_data(x, v)
    return line, line_exact,

anim = FuncAnimation(fig, update, frames=T, interval=1, repeat=False, blit=True)

plt.show()
