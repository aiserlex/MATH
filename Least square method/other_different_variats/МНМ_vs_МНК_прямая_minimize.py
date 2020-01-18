import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize


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

        def func_mod(c):
            s = 0
            for i in range(len(x)):
                s = s + abs(c[0] * x[i] + c[1] - y[i])
            return s

        def func_kv(c):
            s = 0
            for i in range(len(x)):
                s = s + (c[0] * x[i] + c[1] - y[i]) ** 2
            return s


        x0 = np.array([1, 1])
        res_mod = minimize(func_mod, x0, method='nelder-mead',
                       options={'xtol': 1e-8, 'disp': False})

        res_kv = minimize(func_kv, x0, method='nelder-mead',
                       options={'xtol': 1e-8, 'disp': False})

        a_mod, b_mod = res_mod.x
        a_kv, b_kv = res_kv.x

        t = np.linspace(*xlims)

        z_mod = a_mod * t + b_mod
        z_kv = a_kv * t + b_kv

        line_mod.set_data(t, z_mod)
        line_kv.set_data(t, z_kv)

    fig.canvas.draw_idle()


if __name__ == "__main__":
    fig, ax = plt.subplots()

    ax.grid(True)
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_aspect('equal')
    line_mod, = ax.plot([], [], 'b', label='mod')
    line_kv, = ax.plot([], [], 'g', label='kv')

    fig.canvas.mpl_connect('button_press_event', onclick)
    ax.legend()

    plt.show()
