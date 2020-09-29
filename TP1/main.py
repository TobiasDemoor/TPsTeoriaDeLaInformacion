import random
import math 
import pandas
from fuentesDeInfo import Dist, DistExp, DistExpFactory, DistSimulada, DistTeoricaDiscreta

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
print(f"H(S2) = {d2.entropia()}")
print(d2.reporte())
print(f"H(S3) = {d3.entropia()}")
print(d3.reporte())
