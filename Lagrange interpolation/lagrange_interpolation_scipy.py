import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import lagrange

xlims = (-5, 5)
ylims = (-5, 5)
x = []
y = []


def onclick(event):
    ax.plot((event.xdata), (event.ydata), 'r.')
    x.append(event.xdata)
    y.append(event.ydata)
    n = len(x)
    if n >= 2:
        a = lagrange(x, y)
        line.set_data(t, a(t))
    fig.canvas.draw_idle()


if __name__ == "__main__":
    fig, ax = plt.subplots()

    ax.grid(True)
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_aspect('equal')
    line, = ax.plot([], [], 'b')
    t = np.linspace(*xlims, 1000)
    # ax.plot(t, np.sin(t))
    fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()
