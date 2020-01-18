from functools import partial
import matplotlib.pyplot as plt
import numpy as np

xlims = (-5, 5)
ylims = (-5, 5)
x = []
y = []


def onclick(event):
    ax.plot((event.xdata), (event.ydata), 'g.')
    x.append(event.xdata)
    y.append(event.ydata)
    n = len(x)
    if n >= 2:
        x2 = sum(map(lambda x: x ** 2, x))
        xy = np.dot(x, y)

        a = (n*xy - sum(x)*sum(y)) / (n*x2 - sum(x)**2)
        b = (sum(y) - a*sum(x)) / n

        t = np.linspace(*xlims)
        z = a * t + b
        line.set_data(t, z)
    fig.canvas.draw_idle()


if __name__ == "__main__":
    fig, ax = plt.subplots()

    ax.grid(True)
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_aspect('equal')
    line, = ax.plot([], [], 'b')
    fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()
