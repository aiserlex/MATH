import matplotlib.pyplot as plt
import numpy as np
import random


XLIM = (-4, 4)
YLIM = (-4, 4)


def draw():
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
        linep.set_data([], [])
    else:
        ax.set_title(f'Нет пересечений, dist={round(np.hypot((xl-xc), (yl-yc)), 2)}')
        dotl.set_data([xl], [yl])
        dotc.set_data([xc], [yc])
        linep.set_data([xl, xc], [yl, yc])
    
    fig.canvas.draw_idle()
    


def onclick(event):
    global x0, y0, x1, y1, x2, y2, r0
    x0 = random.random()*(XLIM[1]-XLIM[0])-(XLIM[1]-XLIM[0])/2
    y0 = random.random()*(YLIM[1]-YLIM[0])-(YLIM[1]-YLIM[0])/2
    r0 = random.random() * min(x0-XLIM[0], XLIM[1]-x0, y0-YLIM[0], YLIM[1]-y0) + 0.1
    x1 = event.xdata
    y1 = event.ydata
    x2 = event.xdata
    y2 = event.ydata
    draw()
    

def onmove(event):
    global x0, y0, x1, y1, x2, y2, r0
    if not event.inaxes:
        return
    if x0 == 0:
        return
    x2 = event.xdata
    y2 = event.ydata
    draw()


x0 = 0; y0 = 0
x1 = 0; y1 = 0
x2 = 0; y2 = 0
r0 = 0

fig = plt.figure()
fig.canvas.mpl_connect('motion_notify_event', onmove)
fig.canvas.mpl_connect('button_press_event', onclick)

ax = fig.add_subplot(111, xlim=XLIM, ylim=YLIM)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [], 'r')
linep, = ax.plot([], [], 'g')
circ = ax.add_artist(plt.Circle((0, 0), 0))
dotl, = ax.plot([], [], '.g')
dotc, = ax.plot([], [], '.g')

plt.show()
