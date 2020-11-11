from fuentesDeInfo import FuenteDeInfo, FuenteDeInfoFactory
import matplotlib.pyplot as plt
from random import random

def inversa(self, prob):
    acum = 0
    for i in self.ids:
        acum += self.prob(i)
        if acum > prob:
            return i

    return self.ids[-1]

fuente = FuenteDeInfoFactory.crear(
    [1,2,3,4,5,6,7],
    [0.142, 0.0519, 0.00323, 0.245, 0.0587, 0.387, 0.11217]
)

fig, ax = plt.subplots()

style = "k-"

acum = 0
anti = 0
for i in fuente.ids:
    ant = acum
    acum += fuente.prob(i)
    ax.plot([i,i], [ant, acum], style)
    if anti:
        ax.plot([anti, i], [ant, ant], style)
    anti = i
ax.plot([anti, 8], [1,1], style)
y = 0.67
inv = inversa(fuente, y)
ax.plot([0, inv], [y,y], style+'-')
ax.plot([inv, inv], [y, 0], style+'-')

ax.set_xticklabels(['', 'a', 'b', 'c', 'd', 'e', 'f', 'g'])
ax.set_xlim(0, 8)
ax.set_ylim(0, 1.1)

plt.grid()
plt.show()