import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad


def cos2(x):
    return np.cos(x**2)


def sin2(x):
    return np.sin(x**2)


param = np.linspace(-7, 7, 700)

x = [quad(cos2, 0, val)[0] for val in param]
y = [quad(sin2, 0, val)[0] for val in param]

fig, ax = plt.subplots()

ax.axhline(y=0, color='k', lw=0.5)
ax.axvline(x=0, color='k', lw=0.5)
ax.axis('equal')
ax.grid()

ax.plot(x, y)
plt.show()
