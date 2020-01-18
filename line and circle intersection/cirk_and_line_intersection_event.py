import matplotlib.pyplot as plt
import numpy as np
import random


XLIM = (-4, 4)
YLIM = (-4, 4)


def onclick(event):
    x0, x1, x2 = [random.random()*(XLIM[1]-XLIM[0])-(XLIM[1]-XLIM[0])/2
        for _ in range(3)]
    y0, y1, y2 = [random.random()*(YLIM[1]-YLIM[0])-(YLIM[1]-YLIM[0])/2
        for _ in range(3)]
    r0 = random.random() * min(x0-XLIM[0], XLIM[1]-x0, y0-YLIM[0], YLIM[1]-y0) + 0.1
    
    # print(x0, x1, x2)
    # print(y0, y1, y2)
    # print(r0)
    # print()
    
    circ.set_radius(r0)
    circ.set_center((x0, y0))
    line.set_data([x1, x2], [y1, y2])
    
    a = (x2-x1)**2 + (y2-y1)**2
    b = 2*((x2-x1)*(x1-x0)+(y2-y1)*(y1-y0))
    c = (x1-x0)**2+(y1-y0)**2

    tv = -b/(2*a)
    
    if tv < 0:
        tv = 0
    elif tv > 1:
        tv = 1
        
    yv = a*tv**2+b*tv+c
        
    xl = x1 + tv*(x2-x1)
    yl = y1 + tv*(y2-y1)
    
    hypotl = np.hypot((xl-x0), (yl-y0))
    cosp = (xl-x0) / hypotl
    sinp = (yl-y0) / hypotl
    
    xc = r0 * cosp + x0
    yc = r0 * sinp + y0
    
    if yv <= r0**2:
        ax.set_title('Есть пересечение.')
        dotl.set_data([], [])
        dotc.set_data([], [])
    else:
        ax.set_title('Нет пересечений.')
        dotl.set_data([xl], [yl])
        dotc.set_data([xc], [yc])
    
    fig.canvas.draw_idle()
    

fig = plt.figure()
fig.canvas.mpl_connect('button_press_event', onclick)

ax = fig.add_subplot(111, xlim=XLIM, ylim=YLIM)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'r')
circ = ax.add_artist(plt.Circle((0, 0), 0))
dotl, = ax.plot([], [], '.g')
dotc, = ax.plot([], [], '.g')

plt.show()
