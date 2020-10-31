from math import ceil
from fuentesDeInfo import FuenteDeInfo, FuenteDeInfoFactory
import pandas as pd


class CodigoBloque:
    """Clase que representa un código bloque"""

    def __init__(self, fuente, codigos):
        self.fuente = fuente
        self.codigos = codigos

    def codigo(self, id) -> str:
        """Retorna el código asociado a un símbolo id"""

        return self.codigos[id]

    def listaCodigos(self) -> list:
        """Retorna los códigos del código bloque en una lista"""

        return list(self.codigos.values())
    
    def entropia(self) -> float:
        return self.fuente.entropia()

    def longMedia(self):
        """Calcula la longitud media del Código Bloque"""

        res = 0
        for i in self.fuente.ids:
            res += self.fuente.prob(i) * len(self.codigos[i])
        return res

    def rendimiento(self):
        return self.fuente.entropia()/self.longMedia()

    def redundancia(self):
        return 1-self.rendimiento()
        
    def reporte(self) -> tuple:
        """
            Genera un reporte del Código Bloque
            Retorna una tupla como al siguiente
            (
                reporte entropia de la fuente: string,
                tabla de reporte por simbolo: pandas.Dataframe,
                reporte de longitud media: string,
                reporte de si es compacto: string,
                reporte de si cumple la inecuación de kraft: string
            )
        """

        entropia, df = self.fuente.reporte()
        df.insert(1, "Codigo", list(map(lambda x: self.codigos[x], self.fuente.ids)))
        longM = f"\nLongitud media: {self.longMedia()}"
        comp = f"\nEs compacto: {esCompacto(self)}"
        kraft = f"\nCumple Kraft: {cumpleKraft(self, 2)}"
        return entropia, df, longM, comp, kraft



class CodigoBloqueFactory:

    @staticmethod
    def crear(ids: list, codigos: list, probs: list) -> CodigoBloque:
        """
            Genera un objeto CodigoBloque a partir de sus ids,
            codigos y probabilidades asociadas
        """

        fuente = FuenteDeInfoFactory.crear(ids, probs)
        dcodigos = {i:j for i, j in zip(ids, codigos)}
        return CodigoBloque(fuente, dcodigos)

    @staticmethod
    def creaCodif(fuente: FuenteDeInfo) -> CodigoBloque:
        """
            Genera un objeto CodigoBloque a partir de una fuente
            siendo el código generado binario e instantaneo
        """

        dic = {i : ceil(fuente.cantInformacion(i)) for i in fuente.ids}
        sig, ant = "", 0
        for k, v in sorted(dic.items(), key = lambda x: x[1]):
            if v == 0: v = 1
            if v != ant:
                sig += "0" * (v - ant)
                ant = v
            dic[k] = sig
            # bin() devuelve "0bXXXXX" por lo que omitimos los dos primeros valores 
            sig = bin(int(sig, 2)+1)[2:].zfill(v)
        return CodigoBloque(fuente, dic)

    
def esCompacto(codigo: CodigoBloque) -> bool:
    for i  in codigo.fuente.ids:
        if len(codigo.codigo(i)) > ceil(codigo.fuente.cantInformacion(i)):
            return False
    return True


def cumpleKraft(codigo: CodigoBloque, r: int) -> bool:
    suma = 0
    for i in codigo.listaCodigos():
        suma += r**-len(i)
        if round(suma, 2) > 1:
            return False
    return True



