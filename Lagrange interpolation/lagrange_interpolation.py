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
        print("Степень многочлена: {}".format(n - 1))
        l = []
        for i in range(n):
            m = y[i]
            for j in range(n):
                if i != j:
                    m = m * (t - x[j]) / (x[i] - x[j])
            l.append(m)
        z = sum(l)
        line.set_data(t, z)
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
