""" Draw bezier curve using matplotlib.
    Make 4 points using mouse button.
    Move points using mouse to change curve.
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation


XLIM = (-5, 5)
YLIM = (-5, 5)
T = np.linspace(0, 1, 1000)


class App:
    def __init__(self):
        self._fig, self._ax = self._init_axes()
        self._init_artists()

        self._picked = None
        self._dots = []
        self._bezier, = self._ax.plot([], [], 'r')

    def _draw_bezier(self):
        if len(self._dots) == 4:
            centers = [dot.get_center() for dot in self._dots]
            x = (1-T)**3 * centers[0][0] + 3*T*(1-T)**2 * centers[1][0] + 3*T**2*(1-T) * centers[2][0] + T**3 * centers[3][0]
            y = (1-T)**3 * centers[0][1] + 3*T*(1-T)**2 * centers[1][1] + 3*T**2*(1-T) * centers[2][1] + T**3 * centers[3][1]
            self._bezier.set_data(x, y)
        else:
            self._bezier.set_data([], [])

    def _init_artists(self):
        pass

    def _init_axes(self):
        fig, ax = plt.subplots()

        ax.grid()
        ax.set_xlim(XLIM)
        ax.set_ylim(YLIM)
        ax.set_aspect("equal")

        ax.set_title("Bezier curve")
        ax.set_xlabel("x axis")
        ax.set_ylabel("y axis")

        fig.canvas.mpl_connect("button_press_event", self._onbtndown)
        fig.canvas.mpl_connect("motion_notify_event", self._onmove)
        fig.canvas.mpl_connect('pick_event', self._onpick)
        fig.canvas.mpl_connect('button_release_event', self._onrelease)

        return fig, ax

    def _onbtndown(self, event):
        if event.inaxes is None:
            return

        if self._picked:
            return

        dot = plt.Circle((event.xdata, event.ydata), radius=0.1, picker=5)
        self._ax.add_patch(dot)
        self._dots.append(dot)

        self._draw_bezier()

        plt.show()

    def _onmove(self, event):
        if event.inaxes is None:
            return

        if self._picked:
            self._picked.set_center((event.xdata, event.ydata))

        self._draw_bezier()

        plt.show()

    def _onpick(self, event):
        self._picked = event.artist

    def _onrelease(self, event):
        self._picked = None

    def show(self):
        plt.show()


if __name__ == "__main__":
    app = App()
    app.show()
