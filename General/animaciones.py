import numpy as np
from markov import FuenteDeMarkov
from random import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ids = ["A", "B", "C", "D"]
# mat = np.array([
#         [0.114, 0.0951, 0.273, 0.536],
#         [0.0074, 0.00755, 0.236, 0.0434],
#         [0.375, 0.0847, 0.189, 0.206],
#         [0.5036, 0.81265, 0.302, 0.2146]
#     ])

ids = ["A", "B", "C", "D", "E"]
mat = np.array([
    [0.163, 0.00693, 0.694, 0.0406, 0.463],
    [0.259, 0.0655, 0.0817, 0.329, 0.099],
    [0.251, 0.514, 0.0517, 0.179, 0.228],
    [0.222, 0.361, 0.00799, 0.0948, 0.1],
    [0.105, 0.05257, 0.16461, 0.3566, 0.11]
])

vects = []
vect = np.zeros_like(ids, 'float64')
vect[0] = 1.0

vects.append(vect)

# creo la cuadrilla
fig = plt.figure()
n = 30
ax = plt.axes(xlim=(0, n), xticks=range(0, n+1, 2), ylim=(0, 1))
lines = []
for i in ids:
    line, = ax.plot([], [], lw=2)
    line.set_label(i)
    lines.append(line)
ax.legend()


def init():
    global lines
    # la inicializa
    for line in lines:
        line.set_data([], [])
    return tuple(lines)


def animate(i):
    global vects, lines
    # arma cada frame
    if i == 0:
        vect = np.zeros_like(ids, 'float64')
        vect[0] = 1.0
        vects = [vect]
    vect = mat.dot(vects[-1])
    vects.append(vect)
    long = len(vects)
    x = np.array(range(long))
    for i, line in enumerate(lines):
        line.set_data(x, np.array([v[i] for v in vects]))

    return tuple(lines)


# creo el objeto animacion
anim = animation.FuncAnimation(
    fig, animate, init_func=init, frames=30, interval=120, blit=True
)

# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
# anim.save('im.mp4', writer=writer)
plt.show()
