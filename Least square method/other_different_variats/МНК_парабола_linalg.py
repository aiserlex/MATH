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
    if n >= 3:
        x1 = sum(x)
        x2 = sum(map(lambda x: x ** 2, x))
        x3 = sum(map(lambda x: x ** 3, x))
        x4 = sum(map(lambda x: x ** 4, x))
        y1 = sum(y)
        xy = np.dot(x, y)
        x2y = np.dot(list(map(lambda x: x ** 2, x)), y)

        A = np.array([[x4, x3, x2], [x3, x2, x1], [x2, x1, n]])
        B = np.array([x2y, xy, y1])

        a, b, c = np.linalg.solve(A, B)

        t = np.linspace(*xlims)
        z = a * t ** 2 + b * t + c
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
