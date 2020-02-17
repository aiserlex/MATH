import matplotlib.pyplot as plt
import cmath
from collections import defaultdict


ZXLIM = (-10, 10)
ZYLIM = (-10, 10)

WXLIM = (-10, 10)
WYLIM = (-10, 10)

COLORS = 'rgbmck'


def func(z):
    return cmath.exp(z)
    # return cmath.sin(z)
    # return z**2
    # return z**3


class App:
    def __init__(self):
        self.fig = plt.figure(figsize=(8, 4))
        plt.suptitle('АНАЛИЗ КОМПЛЕКСНОЙ ФУНКЦИИ $w = w(z)$')
        plt.subplots_adjust(wspace = 0.4)

        self.ax_z = self.tune_zaxis()
        self.ax_w = self.tune_waxis()

        self.data_z1 = defaultdict(list)
        self.data_z2 = defaultdict(list)
        self.data_w1 = defaultdict(list)
        self.data_w2 = defaultdict(list)

        self.lines_counter = -1

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onmove)

    def tune_zaxis(self):
        ax = self.fig.add_subplot(121)
        ax.grid()
        ax.axis('square')
        ax.set_xlim(ZXLIM)
        ax.set_ylim(ZYLIM)
        ax.set_xlabel('$Re(z)$')
        ax.set_ylabel('$Im(z)$')
        ax.set_title('Прообраз, $z$')
        return ax

    def tune_waxis(self):
        ax = self.fig.add_subplot(122)
        ax.grid()
        ax.axis('square')
        ax.set_xlim(WXLIM)
        ax.set_ylim(WYLIM)
        ax.set_xlabel('$Re(w)$')
        ax.set_ylabel('$Im(w)$')
        ax.set_title('Образ, $w$')
        return ax

    def onmove(self, event):
        if event.inaxes != self.ax_z:
            return

        z = complex(event.xdata, event.ydata)
        w = func(z)

        if event.button == 1:
            self.data_z1[self.lines_counter].append(z.real)
            self.data_z2[self.lines_counter].append(z.imag)

            self.data_w1[self.lines_counter].append(w.real)
            self.data_w2[self.lines_counter].append(w.imag)

        for i in range(2):
            for line in self.ax_z.lines:
                line.remove()

        for i in range(2):
            for line in self.ax_w.lines:
                line.remove()

        self.ax_z.plot([z.real], [z.imag], '.m')
        self.ax_w.plot([w.real], [w.imag], '.m')

        for i in range(self.lines_counter + 1):
            self.ax_z.plot(self.data_z1[i], self.data_z2[i], color=COLORS[i%len(COLORS)], lw=1)
            self.ax_w.plot(self.data_w1[i], self.data_w2[i], color=COLORS[i%len(COLORS)], lw=1)

        self.fig.canvas.draw()

    def onclick(self, event):
        if event.button == 1:
            self.lines_counter += 1

    def show(self):
        plt.show()


if __name__ == "__main__":
    app = App()
    app.show()
