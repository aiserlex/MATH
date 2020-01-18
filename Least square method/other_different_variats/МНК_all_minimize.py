from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


xlims = (-5, 5)
ylims = (-5, 5)
x = []
y = []
x0 = np.array([1, 1, 1])


def f(x, c):
    return c[0] * x**2 + c[1] * x + c[2]


def F(c):
    s = 0
    for i in range(len(x)):
        s = s + (f(x[i], c) - y[i]) ** 2
    return s


def onclick(event):
    ax.plot((event.xdata), (event.ydata), 'g.')
    x.append(event.xdata)
    y.append(event.ydata)
    n = len(x)
    if n >= 2:

        res = minimize(F, x0, method='nelder-mead',
                       options={'xtol': 1e-8, 'disp': False})
        c = res.x

        t = np.linspace(*xlims)
        z = f(t, c)

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
