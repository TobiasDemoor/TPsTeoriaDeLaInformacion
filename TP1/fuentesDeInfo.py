from random import random
import pandas as pd
from math import log2
from SIM import Dist, DistExp, DistExpFactory, DistSimulada, DistTeoricaDiscreta


def binaria(w: float) -> DistExp:
    """Método factory para una distribución binaria con P(0) = w"""

    return DistExp([0,1], [w ,1])

def entropiaBin(w: float) -> float:
    """Método para calcular la entropía de una distribución binaria con P(0) = w"""

    if (w == 0) or (w == 1): return 0
    return w*-log2(w)+(1-w)*-log2(1-w)

def secuencia(self: Dist, n: int) -> list:
    """Genera una secuencia de n valores al azar según la distribución"""
    
    rand = []
    for _ in range(n):
        rand.append(random())
    return self.simulacion(rand)

def cantInformacion(self: Dist, dato) -> float:
    """Calcula la cantidad de información en bits de un dato dado"""
    p = self.prob(dato)
    if p == 0: 
        retorno = 0
    else: 
        retorno = log2(1/p)
    return retorno

def entropia(self: Dist) -> float:
    ent = 0
    for i in self.valores:
        ent += self.prob(i)*self.cantInformacion(i)
    return ent

def reporte(self: Dist) -> pd.DataFrame:
    return pd.DataFrame({
        "Dato":self.valores, 
        "Probabilidad":list(map(self.prob, self.valores)), 
        "Información": list(map(self.cantInformacion, self.valores))
        })


def extensionDeFuente(fuente: Dist, orden:int):
    valoresAnt, probAnt = fuente.valores, list(map(fuente.prob, fuente.valores))
    for __ in range(1, orden):
        valores, prob = [], []
        for i, k in enumerate(valoresAnt):
            for j, l in enumerate(fuente.valores):
                valores.append(str(k)+str(l))
                prob.append(probAnt[i]*fuente.prob(fuente.valores[j]))
        probAnt = prob
        valoresAnt = valores
        
    return DistExpFactory.fromProbAbs(valoresAnt, probAnt)




#Se añaden las funciones a la clase Dist dinámicamente
Dist.secuencia = secuencia
Dist.cantInformacion = cantInformacion
Dist.entropia = entropia
Dist.reporte = reporte

DistExpFactory.binaria = binaria