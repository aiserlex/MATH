import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def update(frame):
    global end
    if frame == end * 10:
        end = 2 * end
        ax.set_xlim((0, end))
        ax.set_aspect('equal')
    t_end = frame / 10
    circ.set_center((t_end, 1))
    t = np.linspace(0, t_end, 1000)
    x = t - np.sin(t)
    y = 1 - np.cos(t)

    dot.set_data([x[-1]], [y[-1]])
    line.set_data(x, y)
    return circ, line, dot

end = 15
fig = plt.figure()
ax = fig.add_subplot(111, xlim=(0, end), ylim=(-1, 3))
ax.set_aspect('equal')
ax.grid()
circ = ax.add_artist(plt.Circle((0, 0), 1))
line, = ax.plot([], [], 'g')
dot, = ax.plot([], [], '.r')

anim = FuncAnimation(fig, update, interval=40)
plt.show()
