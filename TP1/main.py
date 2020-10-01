import random
import math 
import pandas
from fuentesDeInfo import Dist, DistExp, DistExpFactory, DistSimulada, DistTeoricaDiscreta
from markov import FuenteDeMarkov
import graphviz
# Anexo 1
d1 = DistExpFactory.fromProbAbs(
    ['a', 'b', 'c', 'd'],
    [0.605, 0.108, 0.174, 0.113]
)
d2 = DistExpFactory.fromProbAbs(
    ['a', 'b', 'c', 'd', 'e'],
    [0.0446, 0.211, 0.338, 0.331, 0.0754]
)
d3 = DistExpFactory.fromProbAbs(
    ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    [0.142, 0.0519, 0.00323, 0.245, 0.0587, 0.387, 0.11217]
)

print(f"H(S1) = {d1.entropia()}")
print(d1.reporte())
print(f"\nH(S2) = {d2.entropia()}")
print(d2.reporte())
print(f"\nH(S3) = {d3.entropia()}")
print(d3.reporte())




# Anexo 2
markov1 = FuenteDeMarkov(
    ["A", "B", "C", "D"],
    [
        [0.114, 0.0951, 0.273, 0.536 ],
        [0.0074, 0.00755, 0.236, 0.0434 ],
        [0.375, 0.0847, 0.189, 0.206 ],
        [0.5036, 0.81265, 0.302, 0.2146]
    ])

markov2 = FuenteDeMarkov(
    ["A", "B", "C", "D", "E"],
    [
        [0.163, 0.00693, 0.694, 0.0406, 0.463],
        [0.259, 0.0655, 0.0817, 0.329, 0.099],
        [0.251, 0.514, 0.0517, 0.179, 0.228],
        [0.222, 0.361, 0.00799, 0.0948, 0.1],
        [0.105, 0.05257, 0.16461, 0.3566, 0.11]
    ])

print(f"\nFuente N°1: {markov1.vectorEstacionario}")
print(f"\nFuente N°2: {markov2.vectorEstacionario}")

# markov1.grafo.render("grafo1")
# markov2.grafo.render("grafo2")
# print("\nSe pueden visualizar los grafos en los pdf generados generados.")