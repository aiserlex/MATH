import tkinter as tk

from math import tan, sin, cos, pi


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
FPS = 30


class Point:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def __repr__(self):
        return f"Point({round(self._x, 2)}, {round(self._y, 2)}, {round(self._z, 2)})"


    def __getitem__(self, index):
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        elif index == 2:
            return self._z
        else:
            raise Exception("Index out of bounds")

    def __setitem__(self, index, value):
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        elif index == 2:
            self._z = value
        else:
            raise Exception("Index out of bounds")


class Triangle:
    def __init__(self, v1, v2, v3):
        self._v1 = v1
        self._v2 = v2
        self._v3 = v3

    def __repr__(self):
        return f"Tri({self._v1}, {self._v2}, {self._v3})"

    def __iter__(self):
        yield self._v1
        yield self._v2
        yield self._v3

    def __getitem__(self, index):
        if index == 0:
            return self._v1
        elif index == 1:
            return self._v2
        elif index == 2:
            return self._v3
        else:
            raise Exception("Index out of bounds")

    @property
    def points(self):
        return [v for v in self]

class Cube:
    def __init__(self):
        v1 = Point(-1, -1, -1)
        v2 = Point(-1, 1, -1)
        v3 = Point(1, 1, -1)
        v4 = Point(1, -1, -1)
        v5 = Point(-1, -1, 1)
        v6 = Point(-1, 1, 1)
        v7 = Point(1, 1, 1)
        v8 = Point(1, -1, 1)

        t1  = Triangle(v1, v2, v3)
        t2  = Triangle(v1, v3, v4)
        t3  = Triangle(v4, v3, v7)
        t4  = Triangle(v4, v7, v8)
        t5  = Triangle(v2, v6, v7)
        t6  = Triangle(v2, v7, v3)
        t7  = Triangle(v1, v4, v8)
        t8  = Triangle(v1, v8, v5)
        t9  = Triangle(v1, v5, v6)
        t10 = Triangle(v1, v6, v2)
        t11 = Triangle(v5, v8, v7)
        t12 = Triangle(v5, v7, v6)

        self._points = [v1, v2, v3, v4, v5, v6, v7, v8]
        self._triangles = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]

    @property
    def points(self):
        return self._points

    @property
    def triangles(self):
        return self._triangles


class Mesh:
    def __init__(self, triangles):
        pass


class Transformations:
    @staticmethod
    def resize_object(list_of_points, scale=1):
        for i in range(len(list_of_points)):
            list_of_points[i][0] *= scale
            list_of_points[i][1] *= scale
            list_of_points[i][2] *= scale

    @staticmethod
    def move_object(list_of_points, x=0, y=0, z=0):
        for i in range(len(list_of_points)):
            list_of_points[i][0] += x
            list_of_points[i][1] += y
            list_of_points[i][2] += z

    @staticmethod
    def rotate_x(list_of_points, angle):
        angle = angle / 180 * pi
        m = [
                [ cos(angle), sin(angle), 0],
                [-sin(angle), cos(angle), 0],
                [          0,          0, 1],
        ]
        for i, p in enumerate(list_of_points):
            t1 = p[0]*m[0][0] + p[1]*m[1][0] + p[2]*m[2][0]
            t2 = p[0]*m[0][1] + p[1]*m[1][1] + p[2]*m[2][1]
            t3 = p[0]*m[0][2] + p[1]*m[1][2] + p[2]*m[2][2]
            list_of_points[i][0] = t1
            list_of_points[i][1] = t2
            list_of_points[i][2] = t3

    @staticmethod
    def rotate_y(list_of_points, angle):
        angle = angle / 180 * pi
        m = [
                [ cos(angle), 0, sin(angle)],
                [          0, 1,          0],
                [-sin(angle), 0, cos(angle)],
        ]
        for i, p in enumerate(list_of_points):
            t1 = p[0]*m[0][0] + p[1]*m[1][0] + p[2]*m[2][0]
            t2 = p[0]*m[0][1] + p[1]*m[1][1] + p[2]*m[2][1]
            t3 = p[0]*m[0][2] + p[1]*m[1][2] + p[2]*m[2][2]
            list_of_points[i][0] = t1
            list_of_points[i][1] = t2
            list_of_points[i][2] = t3

    @staticmethod
    def rotate_z(list_of_points, angle):
        angle = angle / 180 * pi
        m = [
                [1,           0,          0],
                [0,  cos(angle), sin(angle)],
                [0, -sin(angle), cos(angle)],
        ]
        for i, p in enumerate(list_of_points):
            t1 = p[0]*m[0][0] + p[1]*m[1][0] + p[2]*m[2][0]
            t2 = p[0]*m[0][1] + p[1]*m[1][1] + p[2]*m[2][1]
            t3 = p[0]*m[0][2] + p[1]*m[1][2] + p[2]*m[2][2]
            list_of_points[i][0] = t1
            list_of_points[i][1] = t2
            list_of_points[i][2] = t3


class PProjector:
    def __init__(self, w, h, angle, z_near, z_far):
        ar = h / w
        angle = angle / 180 * pi
        fov = 1 / tan(angle / 2)
        q = z_far / (z_far - z_near)
        self._pmatrix = [
            [ar * fov, 0,   0,           0],
            [0,        fov, 0,           0],
            [0,        0,   q,           1],
            [0,        0,   -q * z_near, 0],
        ]

    def project_point(self, point):
        p = point
        m = self._pmatrix
        x = p[0]*m[0][0] + p[1]*m[1][0] + p[2]*m[2][0] + m[3][0]
        y = p[0]*m[0][1] + p[1]*m[1][1] + p[2]*m[2][1] + m[3][1]
        z = p[0]*m[0][2] + p[1]*m[1][2] + p[2]*m[2][2] + m[3][2]
        w = p[0]*m[0][3] + p[1]*m[1][3] + p[2]*m[2][3] + m[3][3]
        if w != 0:
            x /= w
            y /= w
            z /= w
        return Point(x, y, z)

    def project_triangle(self, triangle):
        point1, point2, point3 = triangle
        p1 = self.project_point(point1)
        p2 = self.project_point(point2)
        p3 = self.project_point(point3)
        return Triangle(p1, p2, p3)


class Window:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("3D engine")
        self._canvas = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self._canvas.pack()
        self._canvas.focus_force()
        self._canvas.bind("<KeyPress>", self._onkeydown)
        self._canvas.bind("<KeyRelease>", self._onkeyup)

    def _onkeydown(self, event):
        pass

    def _onkeyup(self, event):
        pass

    def mainloop(self):
        self._root.mainloop()

    @property
    def root(self):
        return self._root

    @property
    def canvas(self):
        return self._canvas


class Main(Window):
    def __init__(self):
        super().__init__()
        self._history = []
        self._projector = PProjector(
            CANVAS_WIDTH,
            CANVAS_HEIGHT,
            90,
            0.1,
            1000,
        )
        self._angle = 0
        self._draw()

    def _onkeydown(self, event):
        if not event.keysym in self._history:
            self._history.append(event.keysym)

    def _onkeyup(self, event):
        if  event.keysym in self._history:
            self._history.pop(self._history.index(event.keysym))

    def _draw(self):
        if "Left" in self._history:
            print("Left")

        if "Right" in self._history:
            print("Right")

        if "w" in self._history:
            pass

        if "s" in self._history:
            pass

        if "a" in self._history:
            pass

        if "d" in self._history:
            pass

        self._angle += 2

        cube = Cube()

        Transformations.rotate_x(cube.points, self._angle)
        Transformations.rotate_y(cube.points, self._angle)
        Transformations.rotate_z(cube.points, self._angle)

        Transformations.move_object(cube.points, z=10)

        self.canvas.delete("all")
        for triangle in cube.triangles:
            priangle = self._projector.project_triangle(triangle)

            Transformations.resize_object(priangle.points, scale=1000)
            Transformations.move_object(priangle.points, x=200, y=200)

            self.canvas.create_polygon(
                priangle[0][0],
                priangle[0][1],
                priangle[1][0],
                priangle[1][1],
                priangle[2][0],
                priangle[2][1],
                fill="",
                outline="black",
            )

        self.root.after(round(1000/FPS), self._draw)


if __name__ == "__main__":
    main = Main()
    main.mainloop()
