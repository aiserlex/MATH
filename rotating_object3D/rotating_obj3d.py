""" Keys to control 3D object:
    Up, Down, Left, Right, w, s, a, d.
"""

import tkinter as tk

from math import sin, cos, pi, hypot


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
FPS = 30


class Vec(list):
    def __add__(self, arg):
        if len(self) != len(arg):
            raise Exception("Adding Vecs of different lengths.")
        return Vec([self[i] + arg[i] for i in range(len(self))])

    def __sub__(self, arg):
        if len(self) != len(arg):
            raise Exception("Subtracting Vecs of different lengths.")
        return Vec([self[i] - arg[i] for i in range(len(self))])

    def rotate(self, *, phi_x=0, phi_y=0, phi_z=0):
        phi_x = phi_x / 180 * pi
        phi_y = phi_y / 180 * pi
        phi_z = phi_z / 180 * pi

        cx = cos(phi_x)
        sx = sin(phi_x)
        cy = cos(phi_y)
        sy = sin(phi_y)
        cz = cos(phi_z)
        sz = sin(phi_z)

        x = self[0]
        y = self[1]
        z = self[2]

        self[0] = cy*(sz*y + cz*x) - sy*z
        self[1] = sx*(cy*z + sy*(sz*y + cz*x)) + cx*(cz*y - sz*x)
        self[2] = cx*(cy*z + sy*(sz*y + cz*x)) - sx*(cz*y - sz*x)

    def scale(self, scale):
        self[0] *= scale
        self[1] *= scale
        self[2] *= scale

    def shift(self, *, dx=0, dy=0, dz=0):
        self[0] += dx
        self[1] += dy
        self[2] += dz


class Face(list):
    def normal(self):
        vec1 = self[1] - self[0]
        vec2 = self[2] - self[0]
        x = vec1[1]*vec2[2] - vec1[2]*vec2[1]
        y = vec1[2]*vec2[0] - vec1[0]*vec2[2]
        z = vec1[0]*vec2[1] - vec1[1]*vec2[0]
        mod = hypot(x, y, z)
        if mod != 0:
            x /= mod
            y /= mod
            z /= mod
        return Vec([x, y, z])


class Obj3D:
    def __init__(self, filename):
        self._shift_x = 0
        self._shift_y = 0
        self._shift_z = 0

        self._vertices = []
        self._faces = []
        with open(filename) as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                splited = line.split()
                if splited[0] == "v":
                    vertex = Vec(map(float, splited[1:]))
                    self._vertices.append(vertex)
                elif splited[0] == "f":
                    face = Face(map(int, splited[1:]))
                    self._faces.append(face)

        # resolving faces
        for i, face in enumerate(self._faces):
            for j, vertex in enumerate(face):
                self._faces[i][j] = self._vertices[vertex - 1]

    def rotate(self, *, phi_x=0, phi_y=0, phi_z=0):
        for vertex in self._vertices:
            vertex.rotate(phi_x=phi_x, phi_y=phi_y, phi_z=phi_z)
        return self

    def rotate_relto_obj_init(self, *, phi_x=0, phi_y=0, phi_z=0):
        temp_shift_x = self._shift_x
        temp_shift_y = self._shift_y
        temp_shift_z = self._shift_z

        self.shift(dx=-self._shift_x, dy=-self._shift_y, dz=-self._shift_z)
        self.rotate(phi_x=phi_x, phi_y=phi_y, phi_z=phi_z)
        self.shift(dx=temp_shift_x, dy=temp_shift_y, dz=temp_shift_z)
        return self

    def scale(self, scale):
        for vertex in self._vertices:
            vertex.scale(scale)
        return self

    def shift(self, *, dx=0, dy=0, dz=0):
        self._shift_x += dx
        self._shift_y += dy
        self._shift_z += dz
        for vertex in self._vertices:
            vertex.shift(dx=dx, dy=dy, dz=dz)
        return self

    @property
    def vertices(self):
        return self._vertices

    @property
    def faces(self):
        return self._faces


class Window:
    def __init__(self):
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

    def _init_statusbar(self):
        self._statusbar = tk.Label(self._root, anchor=tk.W)
        self._statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_new_status(self, status):
        self._statusbar.config(text=status)

    @property
    def canvas(self):
        return self._canvas

    @property
    def root(self):
        return self._root


class Events:
    def __init__(self, canvas):
        self._keys_pressed = []
        canvas.bind("<KeyPress>", self._onkeydown)
        canvas.bind("<KeyRelease>", self._onkeyup)

    def _onkeydown(self, event):
        if not event.keysym in self._keys_pressed:
            self._keys_pressed.append(event.keysym)

    def _onkeyup(self, event):
        if  event.keysym in self._keys_pressed:
            self._keys_pressed.pop(self._keys_pressed.index(event.keysym))

    @property
    def keys_pressed(self):
        return self._keys_pressed


class Painter:
    def __init__(self, canvas):
        self._canvas = canvas

    @staticmethod
    def _fix_coords(*args):
        new_args = list(args)
        for i in range(0, len(new_args), 2):
            new_args[i] = CANVAS_WIDTH / 2 - new_args[i]
            new_args[i + 1] = CANVAS_HEIGHT / 2 - new_args[i + 1]
        return new_args

    def circle(self, x0, y0, r, fill="green", bd="grey"):
        x0, y0 = self._fix_coords(x0, y0)
        x1 = x0 - r
        y1 = y0 - r
        x2 = x0 + r
        y2 = y0 + r
        self._canvas.create_oval(x1, y1, x2, y2, fill=fill, outline=bd)

    def dot(self, x0, y0, color="black"):
        self.circle(x0, y0, r=3, fill=color, bd=color)

    def polygon(self, *args, fill="green", bd="grey", width=1):
        new_args = self._fix_coords(*args)
        self._canvas.create_polygon(*new_args, fill=fill, outline=bd, width=width)

    def text(self, x0, y0, text):
        x0, y0 = self._fix_coords(x0, y0)
        self._canvas.create_text(x0, y0, text=text, justify=tk.CENTER, font="Verdana 14", fill="blue")


class Scene:
    def __init__(self, camera, screen):
        self._camera = camera  # camera pinhole
        self._screen = screen  # screen position relative to the camera pinhole

    def pprojection(self, vertex):
        """ perspective projection """
        ax, ay, az = vertex
        cx, cy, cz = self._camera
        ex, ey, ez = self._screen

        dx = ax - cx
        dy = ay - cy
        dz = az - cz

        dz = dz if dz != 0 else 0.00001

        bx = ez * dx / dz + ex
        by = ez * dy / dz + ey

        return bx, by, dz

    def oprojection(self, vertex):
        """ orthogonal projection on XOY """
        ax, ay, az = vertex
        return ax, ay, az

    def get_color(self, face):
        face_normal = face.normal()
        mod_scr = hypot(self._screen[0], self._screen[1], self._screen[2])
        mod_scr = mod_scr if mod_scr != 0 else 1
        norm_screen = [self._screen[0]/mod_scr, self._screen[1]/mod_scr, self._screen[2]/mod_scr]
        dot_pr = norm_screen[0]*face_normal[0] + norm_screen[1]*face_normal[1] + norm_screen[2]*face_normal[2]
        if dot_pr >= 0:
            return False
        return "#" + hex(round(abs(dot_pr)*255))[2:]*3

    def skip_out_of_view(self, face):
        face_normal = face.normal()
        dot_pr = face_normal[0]*(face[0][0]-self._camera[0]) + face_normal[1]*(face[0][1]-self._camera[1]) + face_normal[2]*(face[0][2]-self._camera[2])
        if dot_pr > 0:
            return True
        else:
            return False


class Main:
    def __init__(self):
        # init main instruments
        self._window = Window()
        self._painter = Painter(self._window.canvas)
        self._events = Events(self._window.canvas)

        # scene
        self._camera = [0, 0, -1000]
        self._screen = [0, 0, 1000]
        self._light = [0, 0, -1000]
        self._scene = Scene(self._camera, self._screen)

        # init 3D objects
        self._obj = Obj3D("teapot.obj").scale(50).shift(dx=0, dy=0, dz=200)
        self._obj.rotate_relto_obj_init(phi_x=0, phi_y=0)

        self._update()

    def _status(self):
        self._window.set_new_status(f"")

    def _draw(self):
        self._window.canvas.delete("all")

        projected_faces = []
        for face in self._obj.faces:
            color = self._scene.get_color(face)
            if not color:
                continue

            if self._scene.skip_out_of_view(face):
                continue

            projected_face = []
            sum_dz = 0
            for vertex in face:
                bx, by, dz = self._scene.pprojection(vertex)
                projected_face.append(bx)
                projected_face.append(by)
                sum_dz += dz
            projected_face.append(color)
            projected_face.append(sum_dz)
            projected_faces.append(projected_face)
        projected_faces.sort(key=lambda x: -x[-1])

        for projected_face in projected_faces:
            self._painter.polygon(*projected_face[:-2], fill=projected_face[-2], bd=projected_face[-2])

    def handle_events(self):
        if "Up" in self._events.keys_pressed:
            self._obj.rotate_relto_obj_init(phi_x=5)
        if "Down" in self._events.keys_pressed:
            self._obj.rotate_relto_obj_init(phi_x=-5)
        if "Left" in self._events.keys_pressed:
            self._obj.rotate_relto_obj_init(phi_y=5)
        if "Right" in self._events.keys_pressed:
            self._obj.rotate_relto_obj_init(phi_y=-5)
        if "a" in self._events.keys_pressed:
            self._obj.rotate_relto_obj_init(phi_z=5)
        if "d" in self._events.keys_pressed:
            self._obj.rotate_relto_obj_init(phi_z=-5)
        if "w" in self._events.keys_pressed:
            self._obj.shift(dz=-30)
        if "s" in self._events.keys_pressed:
            self._obj.shift(dz=30)

    def mainloop(self):
        self._window.root.mainloop()

    def _update(self):
        self.handle_events()
        self._draw()
        self._status()
        self._window.root.after(round(1000/FPS), self._update)


if __name__ == "__main__":
    main = Main()
    main.mainloop()
