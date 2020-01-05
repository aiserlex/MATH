import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from numpy import pi, sin, cos, sqrt

a = 1  # коэффициент при u_{xx}
xlim = (0, 1)    # область
ylim = (-1, 1)   # интегрирования
tlim = (0, 10)

x = np.linspace(*xlim, 30)
dx = x[1] - x[0]
X = len(x)

t = np.linspace(*tlim, 300)
dt = t[1] - t[0]
T = len(t)

sigma = a * dt / dx
assert a**2 * dt**2 / dx**2 < 1, f"Нарушено условие устойчивости {sigma**2} < 1."

## Реализация численного алгоритма

u = np.zeros((T, X))

u[:, 0] = 0
u[:, X - 1] = 0

u[0, :] = x**2 - x
u[1, :] = u[0, :]

for k in range(1, T - 1):
    for j in range(1, X - 1):
        u[k+1,j] = 2*u[k,j] - u[k-1,j] + a**2*dt**2/dx**2 * (u[k,j+1] - 
                    2*u[k,j] + u[k,j-1]) - 4*u[k,j] * dt**2

## Построение графиков и анимация

fig, ax  = plt.subplots()

ax.grid(True)
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_xlabel('x')
ax.set_ylabel('u(t, x)')

line, = ax.plot([], [], 'b', lw=1, label="численное")
line_exact, = ax.plot([], [], ':r', lw=3, label="точное")
title = ax.text(0.5, 0.92, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5},
                transform=ax.transAxes, ha="center")
ax.legend()

def update(i):
    line.set_data(x, u[i])
    v = -8/pi**3*(cos(sqrt(pi**2+4)*t[i])*sin(pi*x)+1/27*cos(sqrt(9*pi**2+4)*t[i])*sin(3*pi*x))
    line_exact.set_data(x, v)
    title.set_text(f"t={round(t[i], 1):>4}...")
    return line, line_exact, title,

anim = FuncAnimation(fig, update, frames=T, interval=1, repeat=False, blit=True)
anim.save('CHM_z13.mp4', fps=30)

plt.show()
