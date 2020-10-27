from random import random
import pandas as pd
from math import log2
import scipy.stats as stats
import matplotlib.pyplot as plt


class FuenteDeInfo:
    """Clase que representa una fuente de información de memoria nula"""
    def __init__(self, ids, probs):
        self.ids = ids
        self.probs = probs

    def prob(self, id) -> float:
        """Retorna la probabilidad de un símbolo id"""
        return self.probs[id]

    def __inversa(self, prob):
        acum = 0
        for i in self.ids:
            acum += self.prob(i)
            if acum > prob:
                return i

        return self.ids[-1]

    def simulacion(self, n):
        """Genera una colección de valores a partir de una lista de probabilidades"""

        return [self.__inversa(random()) for _ in range(n)]

    def cantInformacion(self, id) -> float:
        """Calcula la cantidad de información en bits de un dato dado"""

        p = self.prob(id)
        if p == 0:
            retorno = 0
        else:
            retorno = log2(1/p)
        return retorno

    def entropia(self) -> float:
        """Calcula la entropia de la fuente"""

        ent = 0
        for i in self.ids:
            ent += self.prob(i)*self.cantInformacion(i)
        return ent

    def reporte(self) -> tuple:
        """
            Genera un reporte de la fuente
            Retorna una tupla como al siguiente
            (
                reporte entropia: string,
                tabla de reporte por simbolo: pandas.Dataframe
            )
        """

        return (f"\nH(S) = {self.entropia()}\n",
            pd.DataFrame({
                "Símbolo": self.ids,
                "Probabilidad": [self.probs[i] for i in self.ids],
                "Información": [self.cantInformacion(i) for i in self.ids]
            }))


class FuenteDeInfoFactory:

    @staticmethod
    def equiprobable(ids):
        """Genera un objeto FuenteDeInfo a partir de sus ids siendo todos equiprobables"""

        p = len(ids)/2
        dprobs = {i: p for i in ids}
        return FuenteDeInfo(ids, dprobs)

    @staticmethod
    def crear(ids, probs):
        """Genera un objeto FuenteDeInfo a partir de sus ids y sus probabilidades absolutas"""

        dprobs = {i: j for i, j in zip(ids, probs)}
        return FuenteDeInfo(ids, dprobs)

    @staticmethod
    def extensionDeFuente(fuente, orden: int):
        """Genera un objeto FuenteDeInfo extension de la fuente "fuente" de orden "orden" """

        idsAnt, probAnt = fuente.ids, [fuente.probs[i] for i in fuente.ids]
        for _ in range(orden-1):
            ids, prob = [], []
            for i, k in enumerate(idsAnt):
                for j, l in enumerate(fuente.ids):
                    ids.append(str(k)+str(l))
                    prob.append(probAnt[i]*fuente.prob(fuente.ids[j]))
            probAnt = prob
            idsAnt = ids

        return FuenteDeInfoFactory.crear(idsAnt, probAnt)

    @staticmethod
    def fromFrecuencia(ids, frecuencias):
        """Genera un objeto FuenteDeInfo a partir de los ids y sus frecuencias"""

        suma = sum(frecuencias)
        prob = [i/suma for i in frecuencias]
        return FuenteDeInfoFactory.crear(ids, prob)

    @staticmethod
    def fromMuestra(muestra):
        """Genera un objeto FuenteDeInfo a partir de una muestra"""

        ids = list(set(muestra))
        ids.sort()
        cant = len(muestra)
        prob = list(map(lambda x: muestra.count(x)/cant, ids))
        return FuenteDeInfoFactory.crear(ids, prob)

    @staticmethod
    def binaria(w: float):
        """Método factory para una distribución binaria con P(0) = w"""

        return FuenteDeInfoFactory.crear([0, 1], [w, 1-w])


def entropiaBin(w: float) -> float:
    """Método para calcular la entropía de una distribución binaria con P(0) = w"""

    if (w == 0) or (w == 1):
        return 0
    return w*-log2(w)+(1-w)*-log2(1-w)


def regr(x, y):
    """
        Método para realizar una regresión lineal retorna la pendiente(m), la ordenada al origen(b)
        y el coeficiente de correlación(r)
    """

    m, b, r, _ = stats.linregress(x, y)
    plt.plot(x, y, 'o')
    ajust = []
    for i in x:
        ajust.append(b + m*i)
    plt.plot(x, ajust, 'r')
    return m, b, r
