import tkinter as tk
from math import *

'''
ПРЕДОПРЕДЕЛЕННЫЕ КОНСТАНТЫ
'''
W, H = (500, 500)  # размеры холста
A, B, C, D = (-5, 5, -5, 5)  # область построения
NX, NY = (10, 10)  # количество узлов координатной сетки
PL, PR, PB, PT = (40, 40, 40, 40)  # поля области построения
ISGRIDON = 1
'''
==========================
'''


'''
ФУНКЦИИ
'''
# трансформация координаты 'x' в координату холста по оси OX
def trmx(x):
    return PL + ((x - A) * W / (B - A)) * ((H - PL - PR) / H)

# трансформация координаты 'y' в координату холста по оси OY
def trmy(y):
    return PT + ((D - y) * H / (D - C)) * ((W - PT - PB) / W)
'''
==========================
'''


'''
ГЛАВНАЯ ПРОГРАММА
'''
# функция пользователя
#func = input('f(x) = ')
func = 'x**3/4 - x'

master = tk.Tk()
canv = tk.Canvas(master, width=W, height=H, bg='lightblue')

# грани области построения графика
canv.create_line(PL, H - PB, W - PR, H - PB)  # нижняя грань
canv.create_line(PL, PT, PL, H - PB)  # левая грань
canv.create_line(PL, PT, W - PR, PT)  # верхняя грань
canv.create_line(W - PR, PT, W - PR, H - PB)  # правая грань

# построение графика
NX2 = NX**3
for i in range(NX2):
    x = A + i * (B - A) / NX2
    y = eval(func.replace('x', '({})'.format(str(x))))
    xnext = A + (i + 1) * (B - A) / NX2
    ynext = eval(func.replace('x', '({})'.format(str(xnext))))
    if (y > D and ynext > D) or (y < C and ynext < C):
        continue
    canv.create_line(trmx(x), trmy(y), trmx(xnext), trmy(ynext))

# коррекция выхода графика на верхнее и нижнее поля
canv.create_rectangle(0, 0, W, PT, fill='lightblue', width=0)
canv.create_rectangle(0, H - PB + 1, W, H, fill='lightblue', width=0)

# риски и подписи по горизонтальной оси
for i in range(NX + 1):
    nodex = A + i * (B - A) / NX
    nodexc = trmx(nodex)
    canv.create_line(nodexc, H - PB - 3, nodexc, H - PB + 3)
    canv.create_text(nodexc, H - PB + 15, text=str(round(nodex, 2)),
                     font=('Arial', 7))
    if ISGRIDON and i > 0 and i < NX:
        canv.create_line(nodexc, H - PB - 6, nodexc, PT,
                         dash=(1, 6), fill='gray')

# риски и подписи по вертикальной оси
for i in range(NY + 1):
    nodey = D - i * (D - C) / NY
    nodeyc = trmy(nodey)
    canv.create_line(PL - 3, nodeyc, PL + 3, nodeyc)
    canv.create_text(PL - 15, nodeyc, text=str(round(nodey, 2)),
                     font=('Arial', 7))
    if ISGRIDON and i > 0 and i < NY:
        canv.create_line(PL + 6, nodeyc, W - PR, nodeyc,
                         dash=(1, 6), fill='gray')

canv.pack()
tk.mainloop()
'''
==========================
'''
