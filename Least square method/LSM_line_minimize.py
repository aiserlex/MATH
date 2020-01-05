import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


xlim = (-4, 4)
ylim = (-4, 4)
x = []
y = []
x0 = [1] * 2


def f(c, x):
    x = np.array(x)
    return c[0] * x + c[1]


def F(c, x, y):
    return np.sum((y - f(c, x))**2)


def onclick(event):

    if not event.inaxes:
        return

    ax.plot(event.xdata, event.ydata, '.g')

    x.append(event.xdata)
    y.append(event.ydata)

    n = len(x)

    if n >= 2:
        rez = minimize(F, x0, (x, y), method='nelder-mead',
                       options={'xtol': 1e-8, 'disp': False})

        line.set_data(t, f(rez.x, t))
    ax.figure.canvas.draw_idle()


if __name__ == '__main__':
    fig, ax = plt.subplots()

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(True)
    ax.set_aspect('equal')

    t = np.linspace(*xlim)
    line, = ax.plot([], [], 'b')
    fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()
