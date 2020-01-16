import tkinter as tk

from math import sin, cos, pi
from PIL import ImageGrab


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
ANIMATION_FPS = 25


class Window:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Cube")
        self._canvas = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self._canvas.pack()

    def mainloop(self):
        self._root.mainloop()

    @property
    def root(self):
        return self._root

    @property
    def canvas(self):
        return self._canvas


class Point:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __repr__(self):
        return f"Point({self._x}, {self._y}, {self._z})"

    def __iter__(self):
        yield self._x
        yield self._y

    def rotate(self, phi, psi, theta):
        # axis x rotation
        y = self._y * cos(phi) + self._z * sin(phi)
        z = -self._y * sin(phi) + self._z * cos(phi)
        self._y = y
        self._z = z

        # axis y rotation
        x = self._x * cos(psi) - self._z * sin(psi)
        z = self._x * sin(psi) + self._z * cos(psi)
        self._x = x
        self._z = z

        # axis z rotation
        x = self._x * cos(theta) + self._y * sin(theta)
        y = -self._x * sin(theta) + self._y * cos(theta)
        self._x = x
        self._y = y

        return self

    def resize(self, scale=1):
        self._x *= scale
        self._y *= scale
        self._z *= scale
        return self

    def shift(self, offset=0):
        self._x += offset
        self._y += offset
        self._z += offset
        return self


class Cube:
    def __init__(self):
        # cube corners
        p1 = Point(-1, -1, -1)
        p2 = Point(1, -1, -1)
        p3 = Point(1, 1, -1)
        p4 = Point(-1, 1, -1)
        p5 = Point(-1, -1, 1)
        p6 = Point(1, -1, 1)
        p7 = Point(1, 1, 1)
        p8 = Point(-1, 1, 1)

        # cube faces
        g1 = [p1, p2, p3, p4]
        g2 = [p1, p5, p8, p4]
        g3 = [p3, p4, p8, p7]
        g4 = [p2, p3, p7, p6]
        g5 = [p1, p2, p6, p5]
        g6 = [p5, p6, p7, p8]

        self._corners = [p1, p2, p3, p4, p5, p6, p7, p8]
        self._faces = [g1, g2, g3, g4, g5, g6]

    def __repr__(self):
        return "\n".join(map(str, self._corners))

    def rotate(self, phi, psi, theta):
        for corner in self._corners:
            corner.rotate(phi, psi, theta)
        return self

    def resize(self, scale=1):
        for corner in self._corners:
            corner.resize(scale)
        return self

    def shift(self, offset=0):
        for corner in self._corners:
            corner.shift(offset)
        return self

    @property
    def corners(self):
        return self._corners

    @property
    def faces(self):
        return self._faces


class Main:
    def __init__(self):
        self._index = 0
        self._phi = 0
        self._psi = 0
        self._theta = 0
        self._window = Window()
        self._draw()
        self._window.mainloop()

    @staticmethod
    def _flatten_list(l):
        return [item for sublist in l for item in sublist]

    def _draw(self):
        self._window.canvas.delete("all")
        self._cube = Cube()
        self._index += 1
        self._phi += 0.02
        self._psi += 0.03
        self._theta += 0.04
        self._cube.rotate(
            self._phi,
            self._psi,
            self._theta,
        )
        self._cube.resize(100).shift(200)
        for face in self._cube.faces:
            self._window.canvas.create_polygon(
                self._flatten_list(face),
                outline="black",
                fill="",
                width=3,
            )
        # self._grab_img(f"imgs/img_{self._index:>05d}.png")  # saving in npg
        self._window.root.after(round(1000 / ANIMATION_FPS), self._draw)

    def _grab_img(self, file_name):
        x = self._window.root.winfo_rootx() + self._window.canvas.winfo_x()
        y = self._window.root.winfo_rooty() + self._window.canvas.winfo_y()
        x1 = x + self._window.canvas.winfo_width()
        y1 = y + self._window.canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_name)


if __name__ == "__main__":
    main = Main()
