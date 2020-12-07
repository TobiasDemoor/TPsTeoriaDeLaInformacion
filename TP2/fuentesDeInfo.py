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

    def cantInformacion(self, id) -> float:
        """Calcula la cantidad de información en bits de un dato dado"""

        p = self.probs[id]
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
            ent += self.probs[i]*self.cantInformacion(i)
        return ent

    def reporte(self) -> pd.DataFrame:
        """
            Genera un reporte de la fuente
            Retorna una tabla de reporte por simbolo: pandas.Dataframe
        """

        return pd.DataFrame({
                "Símbolo": self.ids,
                "Probabilidad": [self.probs[i] for i in self.ids],
                "Información": [self.cantInformacion(i) for i in self.ids]
            })


class FuenteDeInfoFactory:
    @staticmethod
    def crear(ids, probs):
        """Genera un objeto FuenteDeInfo a partir de sus ids y sus probabilidades absolutas"""
        
        dprobs = {i: j for i, j in zip(ids, probs)}
        return FuenteDeInfo(ids, dprobs)
        
    @staticmethod
    def fromMuestra(muestra):
        """Genera un objeto FuenteDeInfo a partir de una muestra"""

        ids = sorted(set(muestra))
        cant = len(muestra)
        prob = [muestra.count(x)/cant for x in ids]
        return FuenteDeInfoFactory.crear(ids, prob)
