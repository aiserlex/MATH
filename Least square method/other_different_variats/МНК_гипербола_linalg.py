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
        obr_x1 = sum(map(lambda x: 1 / x, x))
        obr_x2 = sum(map(lambda x: 1 / x ** 2, x))
        y1 = sum(y)
        y1_obr_x1 = np.dot(y, list(map(lambda x: 1 / x, x)))

        A = np.array([[obr_x2, obr_x1], [obr_x1, n]])
        B = np.array([y1_obr_x1, y1])

        a, b = np.linalg.solve(A, B)

        t = np.linspace(*xlims, 101)
        z = a / t + b
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
