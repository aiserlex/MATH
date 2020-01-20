""" Draw Bezier curves (and the like) using matplotlib.

    Make points using mouse button (4 points for Bezier curve).
    Move points by mouse (drag and drop) to change curve.
    Delete point by right mouse button click on itself.
"""

import matplotlib.pyplot as plt
import numpy as np


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
        self._polyline, = self._ax.plot([], [], 'g', lw=0.5)
        self._cache = {}

    def _draw_bezier(self, x, y):
        self._bezier.set_data(x, y)

    def _get_bezier_rec(self, i=3, j=3):
        if (i, j) not in self._cache:
            if j == 0:
                self._cache[i, j] = self._dots[i].get_center()
            else:
                x = (1-T) * self._get_bezier_rec(i-1, j-1)[0] + T * self._get_bezier_rec(i, j-1)[0]
                y = (1-T) * self._get_bezier_rec(i-1, j-1)[1] + T * self._get_bezier_rec(i, j-1)[1]
                self._cache[i, j] = (x, y)
        return self._cache[i, j]

    def _draw_polyline(self):
        all_x = []
        all_y = []
        for dot in self._dots:
            x, y = dot.get_center()
            all_x.append(x)
            all_y.append(y)
        self._polyline.set_data(all_x, all_y)

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

        if event.button != 1:
            return

        if self._picked:
            return

        dot = plt.Circle((event.xdata, event.ydata), radius=0.1, picker=5)
        self._ax.add_patch(dot)
        self._dots.append(dot)

        if self._dots:
            self._update_drawing()

        plt.show()

    def _onmove(self, event):
        if event.inaxes is None:
            return

        if self._picked:
            self._picked.set_center((event.xdata, event.ydata))

        if self._dots:
            self._update_drawing()

        plt.show()

    def _onpick(self, event):
        if str(event.mouseevent.button) == "MouseButton.LEFT":
            self._picked = event.artist
        elif str(event.mouseevent.button) == "MouseButton.RIGHT":
            self._dots.remove(event.artist)
            self._ax.patches.remove(event.artist)

        if self._dots:
            self._update_drawing()

        plt.show()

    def _onrelease(self, event):
        self._picked = None

    def show(self):
        plt.show()

    def _update_drawing(self):
        self._cache = {}
        x, y = self._get_bezier_rec(len(self._dots) - 1, len(self._dots) - 1)
        self._draw_bezier(x, y)
        self._draw_polyline()


if __name__ == "__main__":
    app = App()
    app.show()
