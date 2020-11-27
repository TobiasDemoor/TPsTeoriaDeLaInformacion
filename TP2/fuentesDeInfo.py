from functools import cached_property
from random import random
import pandas as pd
from math import log2


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

    @cached_property
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

        return (f"\nH(S) = {self.entropia}\n",
            pd.DataFrame({
                "Símbolo": self.ids,
                "Probabilidad": [self.probs[i] for i in self.ids],
                "Información": [self.cantInformacion(i) for i in self.ids]
            }))


class FuenteDeInfoFactory:

    @staticmethod
    def fromMuestra(muestra):
        """Genera un objeto FuenteDeInfo a partir de una muestra"""

        ids = sorted(set(muestra))
        cant = len(muestra)
        prob = [muestra.count(x)/cant for x in ids]
        return FuenteDeInfoFactory.crear(ids, prob)
