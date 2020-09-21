from random import random
import pandas as pd
from math import log2
from SIM import Dist, DistExp, DistExpFactory, DistSimulada, DistTeoricaDiscreta


def secuencia(self: Dist, n: int) -> list:
    """Genera una secuencia de n valores al azar según la distribución"""
    
    rand = []
    for _ in range(n):
        rand.append(random())
    return self.simulacion(rand)


def cantInformacion(self: Dist, dato) -> float:
    """Calcula la cantidad de información en bits de un dato dado"""

    return -log2(self.prob(dato))


def entropia(self: Dist) -> float:
    ent = 0
    for i in self.valores:
        ent += -self.prob(i)*log2(self.prob(i))
    return ent


def reporte(self: Dist) -> pd.DataFrame:
    df = pd.DataFrame({
        "Dato":self.valores, 
        "Probabilidad":list(map(self.prob, self.valores)), 
        "Información": list(map(self.cantInformacion, self.valores))
        })
    return df

#Se añaden las funciones a la clase Dist dinámicamente
Dist.cantInformacion = cantInformacion
Dist.entropia = entropia
Dist.secuencia = secuencia
Dist.reporte = reporte
