from math import log2, ceil
from fuentesDeInfo import FuenteDeInfo, FuenteDeInfoFactory
import pandas as pd

class CodigoBloque:
    def __init__(self, fuente, codigos):
        self.fuente = fuente
        self.codigos = codigos
    
    def codigo(self, id) -> str:
        return self.codigos[id]
    
    def listaCodigos(self) -> list:
        return list(self.codigos.values())
    
    def prob(self, id) -> float:
        return self.fuente.probs(id)

    def reporte(self) -> pd.DataFrame:
        df = self.fuente.reporte()
        df.insert(1, "Codigo", list(map(lambda x: self.codigos[x], self.fuente.ids)))
        return df

    def longMedia(self):
        res = 0
        for i in self.fuente.ids:
            res += self.fuente.prob(i) * len(self.codigos[i])
        return res



class CodigoBloqueFactory:
    @staticmethod
    def equiprobable(ids, codigos):
        fuente = FuenteDeInfoFactory.equiprobable(ids)
        dcodigos = {i: j for i in ids for j in codigos}
        return CodigoBloque(fuente, dcodigos)

    @staticmethod
    def crear(ids, codigos, probs):
        fuente = FuenteDeInfoFactory.crear(ids, probs)
        dcodigos = {i: j for i in ids for j in codigos}
        return CodigoBloque(fuente, dcodigos)

    @staticmethod
    def creaCodif(fuente):
        dic = {i : ceil(-log2(fuente.prob(i))) for i in fuente.ids}
        sig, ant = "", 0
        for k, v in sorted(dic.items(), key = lambda x: x[1]):
            if v != ant:
                sig += "0" * (v-ant)
                ant = v
            dic[k] = sig
            sig = bin(int(sig, 2)+1)[2:].zfill(v)
        return CodigoBloque(fuente, dic)


def cumpleKraft(codigo: CodigoBloque, r: int):
    suma = 0
    for i in codigo.listaCodigos():
        suma += r**-len(i)
        if round(suma, 2) > 1: return False
    return True

    
def esCompacto(codigo: CodigoBloque):
    return codigo.fuente.entropia() <= codigo.longMedia()


def esCodBloque(aCodigo: list, codigo: CodigoBloque) -> bool:
    bloqueaux = codigo.listaCodigos()[:]
    aaux = aCodigo[:]
    longmax = len(max(bloqueaux, key=len))
    it = 0
    while len(bloqueaux) > 0 and it < longmax:
        # remuevo instancias de la extension de orden it+1 del alfabeto
        for i in aaux:
            while i in bloqueaux:
                bloqueaux.remove(i)
        # genero la extension de orden it+2 del alfabeto
        aaux = [i + j for i in aaux for j in aCodigo]
        it += 1
    return len(bloqueaux) == 0


def esNoSingular(codigoBloque: CodigoBloque) -> bool:
    codigos = codigoBloque.listaCodigos()
    return len(set(codigos)) == len(codigos)


def esInstantaneo(codigoBloque: CodigoBloque) -> bool:
    codigos = codigoBloque.listaCodigos()
    for i, x in enumerate(codigos):
        for j, y in enumerate(codigos):
            if y.find(x) == 0 and i != j:
                return False
    return True

