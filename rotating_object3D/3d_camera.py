import numpy as np
import tkinter as tk
from math import log10, pi, cos, sin, tan, atan2, hypot


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
FPS = 30


class Vector4:
    def __init__(self, values):
        self._values = values

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def __mul__(self, arg):
        if type(arg) == Matrix4:
            return Vector4([
                self[0]*arg[0,0] + self[1]*arg[1,0] + self[2]*arg[2,0] + self[3]*arg[3,0],
                self[0]*arg[0,1] + self[1]*arg[1,1] + self[2]*arg[2,1] + self[3]*arg[3,1],
                self[0]*arg[0,2] + self[1]*arg[1,2] + self[2]*arg[2,2] + self[3]*arg[3,2],
                self[0]*arg[0,3] + self[1]*arg[1,3] + self[2]*arg[2,3] + self[3]*arg[3,3],
        ])
        else:
            raise NotImplemented("Can't multiply with non-matrices.")

    def __str__(self):
        return "Vector4({}, {}, {}, {})".format(*self._values)

    __repr__ = __str__

    @classmethod
    def from_xyz(cls, x, y, z):
        return cls([x, y, z, 1])


class Matrix4:
    def __init__(self, values):
        self._values = values

    def __getitem__(self, key):
        return self._values[key[0] * 4 + key[1]]

    def __mul__(self, arg):
        if type(arg) == Matrix4:
            return Matrix4([
                self[0,0]*arg[0,0] + self[0,1]*arg[1,0] + self[0,2]*arg[2,0] + self[0,3]*arg[3,0],
                self[0,0]*arg[0,1] + self[0,1]*arg[1,1] + self[0,2]*arg[2,1] + self[0,3]*arg[3,1],
                self[0,0]*arg[0,2] + self[0,1]*arg[1,2] + self[0,2]*arg[2,2] + self[0,3]*arg[3,2],
                self[0,0]*arg[0,3] + self[0,1]*arg[1,3] + self[0,2]*arg[2,3] + self[0,3]*arg[3,3],

                self[1,0]*arg[0,0] + self[1,1]*arg[1,0] + self[1,2]*arg[2,0] + self[1,3]*arg[3,0],
                self[1,0]*arg[0,1] + self[1,1]*arg[1,1] + self[1,2]*arg[2,1] + self[1,3]*arg[3,1],
                self[1,0]*arg[0,2] + self[1,1]*arg[1,2] + self[1,2]*arg[2,2] + self[1,3]*arg[3,2],
                self[1,0]*arg[0,3] + self[1,1]*arg[1,3] + self[1,2]*arg[2,3] + self[1,3]*arg[3,3],

                self[2,0]*arg[0,0] + self[2,1]*arg[1,0] + self[2,2]*arg[2,0] + self[2,3]*arg[3,0],
                self[2,0]*arg[0,1] + self[2,1]*arg[1,1] + self[2,2]*arg[2,1] + self[2,3]*arg[3,1],
                self[2,0]*arg[0,2] + self[2,1]*arg[1,2] + self[2,2]*arg[2,2] + self[2,3]*arg[3,2],
                self[2,0]*arg[0,3] + self[2,1]*arg[1,3] + self[2,2]*arg[2,3] + self[2,3]*arg[3,3],

                self[3,0]*arg[0,0] + self[3,1]*arg[1,0] + self[3,2]*arg[2,0] + self[3,3]*arg[3,0],
                self[3,0]*arg[0,1] + self[3,1]*arg[1,1] + self[3,2]*arg[2,1] + self[3,3]*arg[3,1],
                self[3,0]*arg[0,2] + self[3,1]*arg[1,2] + self[3,2]*arg[2,2] + self[3,3]*arg[3,2],
                self[3,0]*arg[0,3] + self[3,1]*arg[1,3] + self[3,2]*arg[2,3] + self[3,3]*arg[3,3],
        ])
        else:
            raise NotImplemented("Can't multiply with non-matrices.")

    def __str__(self):
        return "Matrix4([\n\t{} {} {} {}\n\t{} {} {} {}\n\t{} {} {} {}\n\t{} {} {} {}\n])".format(*self._values)

    __repr__ = __str__


class Face(list):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Face(" + ",".join(map(str, self)) + ")"

    __repr__ = __str__


class Obj3d:
    def __init__(self):
        self._vertices = []
        self._faces = []
        with open("scubes.obj") as file:
            for line in file:
                line = line.strip()
                if line:
                    line = line.split()
                    if line[0] == "v":
                        v = Vector4.from_xyz(*list(map(float, line[1:])))
                        self._vertices.append(v)
                    elif line[0] == "f":
                        f = Face(*list(map(int, line[1:])))
                        self._faces.append(f)


        # resolving faces
        for i, face in enumerate(self._faces):
            for j, vertex in enumerate(face):
                self._faces[i][j] = self._vertices[vertex - 1]

    def __str__(self):
        return ", ".join(map(str, self._vertices)) + "\n" + ", ".join(map(str, self._faces))

    __repr__ = __str__

    @property
    def vertices(self):
        return self._vertices

    @property
    def faces(self):
        return self._faces


class Transforms:
    @staticmethod
    def translate(point, a=0, b=0, c=0):
        Tabc = Matrix4([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            a, b, c, 1,
        ])
        return Vector4(point * Tabc)

    @staticmethod
    def scale(point, a=1, b=1, c=1):
        Sabc = Matrix4([
            a, 0, 0, 0,
            0, b, 0, 0,
            0, 0, c, 0,
            0, 0, 0, 1,
        ])
        return Vector4(point * Sabc)

    @staticmethod
    def rotate_z(point, phi=0):
        c = cos(phi)
        s = sin(phi)
        Rz = Matrix4([
             c, s, 0, 0,
            -s, c, 0, 0,
             0, 0, 1, 0,
             0, 0, 0, 1,
        ])
        return Vector4(point * Rz)

    @staticmethod
    def rotate_x(point, phi=0):
        c = cos(phi)
        s = sin(phi)
        Rx = Matrix4([
            1, 0, 0, 0,
            0, c, s, 0,
            0,-s, c, 0,
            0, 0, 0, 1,
        ])
        return Vector4(point * Rx)

    @staticmethod
    def rotate_y(point, phi=0):
        c = cos(phi)
        s = sin(phi)
        Ry = Matrix4([
            c, 0,-s, 0,
            0, 1, 0, 0,
            s, 0, c, 0,
            0, 0, 0, 1,
        ])
        return Vector4(point * Ry)

    @classmethod
    def rotate(cls, point, P, v, phi):
        px = P[0];  py = P[1];  pz = P[2]
        vx = v[0];  vy = v[1];  vz = v[2]
        phi_y = atan2(vx, vz)
        phi_x = atan2(vy, hypot(vx, vz))
        move_to_orig = cls.translate(point, -px, -py, -pz)
        rotate_y = cls.rotate_y(move_to_orig, -phi_y)
        rotate_x = cls.rotate_x(rotate_y, phi_x)
        rotate = cls.rotate_z(rotate_x, phi)
        rotate_x_inv = cls.rotate_x(rotate, -phi_x)
        rotate_y_inv = cls.rotate_y(rotate_x_inv, phi_y)
        move_to_orig_inv = cls.translate(rotate_y_inv, px, py, pz)
        return move_to_orig_inv

    @staticmethod
    def project(point, fov, near, far):
        c = 1 / tan(fov / 2)
        q = (far + near) / (far - near)
        k = 2 * far * near / (far - near)
        P = Matrix4([
            c, 0, 0, 0,
            0, c, 0, 0,
            0, 0, q,-1,
            0, 0, k, 0,
        ])
        rez = point * P
        if rez[3] != 0:
            rez[0] *= 200/rez[3]; rez[1] *= 200/rez[3]; rez[2] *= 200/rez[3]; rez[3] /= rez[3];
        return Vector4(rez)


class Window:
    def __init__(self):
        self._keys_pressed = []

        self._init_window()
        self._init_canvas()
        self._init_statusbar()

    def _init_window(self):
        self._root = tk.Tk()
        self._root.title("3D Engine")

    def _init_canvas(self):
        self._canvas = tk.Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self._canvas.pack()
        self._canvas.focus_force()
        self._canvas.bind("<KeyPress>", self._onkeydown)
        self._canvas.bind("<KeyRelease>", self._onkeyup)

    def _init_statusbar(self):
        self._statusbar = tk.Label(self._root, anchor=tk.W)
        self._statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _onkeydown(self, event):
        if not event.keysym in self._keys_pressed:
            self._keys_pressed.append(event.keysym)

    def _onkeyup(self, event):
        if  event.keysym in self._keys_pressed:
            self._keys_pressed.pop(self._keys_pressed.index(event.keysym))

    def set_new_status(self, status):
        self._statusbar.config(text=status)

    @property
    def canvas(self):
        return self._canvas

    @property
    def root(self):
        return self._root

    @property
    def keys_pressed(self):
        return self._keys_pressed


class Main:
    def __init__(self):
        self._window = Window()
        self._obj = Obj3d()

        # for i, vertex in enumerate(self._obj.vertices):
        #     rez = Transforms.rotate_x(vertex, pi/3)
        #     for j, coord in enumerate(vertex):
        #         vertex[j] = rez[j]
        #
        # for i, vertex in enumerate(self._obj.vertices):
        #     rez = Transforms.rotate_y(vertex, pi/6)
        #     for j, coord in enumerate(vertex):
        #         vertex[j] = rez[j]
        #
        # for i, vertex in enumerate(self._obj.vertices):
        #     rez = Transforms.scale(vertex, 100, 100, 100)
        #     for j, coord in enumerate(vertex):
        #         vertex[j] = rez[j]
        #
        for i, vertex in enumerate(self._obj.vertices):
            rez = Transforms.translate(vertex, 0, 0, -5)
            for j, coord in enumerate(vertex):
                vertex[j] = rez[j]

        # print(self._obj)

    def _handle_events(self):
        if "Up" in self._window.keys_pressed:
            # for i, vertex in enumerate(self._obj.vertices):
            #     rez = Transforms.rotate(vertex, (0,0,0), (1,0,0), pi/100)
            #     for j, coord in enumerate(vertex):
            #         vertex[j] = rez[j]
            pass

        if "Down" in self._window.keys_pressed:
            # for i, vertex in enumerate(self._obj.vertices):
            #     rez = Transforms.rotate(vertex, (0,0,0), (1,0,0), -pi/100)
            #     for j, coord in enumerate(vertex):
            #         vertex[j] = rez[j]
            pass

        if "Left" in self._window.keys_pressed:
            for i, vertex in enumerate(self._obj.vertices):
                rez = Transforms.rotate(vertex, (0,0,0), (0,1,0), -pi/100)
                for j, coord in enumerate(vertex):
                    vertex[j] = rez[j]

        if "Right" in self._window.keys_pressed:
            for i, vertex in enumerate(self._obj.vertices):
                rez = Transforms.rotate(vertex, (0,0,0), (0,1,0), pi/100)
                for j, coord in enumerate(vertex):
                    vertex[j] = rez[j]

        if "a" in self._window.keys_pressed:
            for i, vertex in enumerate(self._obj.vertices):
                rez = Transforms.translate(vertex, .1, 0, 0)
                for j, coord in enumerate(vertex):
                    vertex[j] = rez[j]

        if "d" in self._window.keys_pressed:
            for i, vertex in enumerate(self._obj.vertices):
                rez = Transforms.translate(vertex, -.1, 0, 0)
                for j, coord in enumerate(vertex):
                    vertex[j] = rez[j]

        if "w" in self._window.keys_pressed:
            for i, vertex in enumerate(self._obj.vertices):
                rez = Transforms.translate(vertex, 0, 0, .1)
                for j, coord in enumerate(vertex):
                    vertex[j] = rez[j]

        if "s" in self._window.keys_pressed:
            for i, vertex in enumerate(self._obj.vertices):
                rez = Transforms.translate(vertex, 0, 0, -.1)
                for j, coord in enumerate(vertex):
                    vertex[j] = rez[j]


    def _draw(self):
        self._window.canvas.delete("all")

        for face in self._obj.faces:
            rez_face = []
            for vertex in face:
                rez_face.append(Transforms.project(vertex, pi/2, 0.1, 1000))

            coords = []
            for vertex in rez_face:
                coords.append(CANVAS_WIDTH / 2 + vertex[0])
                coords.append(CANVAS_HEIGHT / 2 - vertex[1])

            self._window.canvas.create_polygon(*coords, fill="", outline="black")

    def update(self):
        self._handle_events()
        self._draw()
        self._window.root.after(round(1000 / FPS), self.update)

    def mainloop(self):
        self._window.root.mainloop()


if __name__ == "__main__":
    m = Main()
    m.update()
    m.mainloop()
