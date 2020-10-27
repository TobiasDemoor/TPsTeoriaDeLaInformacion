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

    def longMedia(self):
        """Calcula la longitud media del Código Bloque"""

        res = 0
        for i in self.fuente.ids:
            res += self.fuente.prob(i) * len(self.codigos[i])
        return res

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
        df.insert(1, "Codigo", list(
            map(lambda x: self.codigos[x], self.fuente.ids)))
        longM = f"\nLongitud media: {self.longMedia()}"
        comp = f"\nEs compacto: {esCompacto(self)}"
        kraft = f"\nCumple Kraft: {cumpleKraft(self, 2)}"
        return entropia, df, longM, comp, kraft


class CodigoBloqueFactory:
    @staticmethod
    def equiprobable(ids: list, codigos: list) -> CodigoBloque:
        """
            Genera un objeto CodigoBloque a partir de sus ids y
            codigos asociados siendo todos equiprobables
        """

        fuente = FuenteDeInfoFactory.equiprobable(ids)
        dcodigos = {i: j for i, j in zip(ids, codigos)}
        return CodigoBloque(fuente, dcodigos)

    @staticmethod
    def crear(ids: list, codigos: list, probs: list) -> CodigoBloque:
        """
            Genera un objeto CodigoBloque a partir de sus ids,
            codigos y probabilidades asociadas
        """

        fuente = FuenteDeInfoFactory.crear(ids, probs)
        dcodigos = {i: j for i, j in zip(ids, codigos)}
        return CodigoBloque(fuente, dcodigos)

    @staticmethod
    def creaCodif(fuente: FuenteDeInfo) -> CodigoBloque:
        """
            Genera un objeto CodigoBloque a partir de una fuente
            siendo el código generado binario e instantaneo
        """

        dic = {i: ceil(fuente.cantInformacion(i)) for i in fuente.ids}
        sig, ant = "", 0
        for k, v in sorted(dic.items(), key=lambda x: x[1]):
            if v == 0:
                v = 1
            if v != ant:
                sig += "0" * (v - ant)
                ant = v
            dic[k] = sig
            # bin() devuelve "0bXXXXX" por lo que omitimos los dos primeros valores
            sig = bin(int(sig, 2)+1)[2:].zfill(v)
        return CodigoBloque(fuente, dic)

    @staticmethod
    def extensionDeFuente(codigoBloque: CodigoBloque, orden: int) -> CodigoBloque:
        """
            Genera un objeto CodigoBloque extension del codigo bloque "codigoBloque"
            de orden "orden"
        """

        fuente = codigoBloque.fuente
        idAnt = fuente.ids
        codAnt = codigoBloque.listaCodigos()
        probAnt = [fuente.prob(i) for i in fuente.ids]
        for _ in range(orden-1):
            ids, cods, probs = [], [], []
            for i, k in enumerate(idAnt):
                for l in fuente.ids:
                    ids.append(str(k)+str(l))
                    cods.append(codAnt[i] + codigoBloque.codigo(l))
                    probs.append(probAnt[i] * fuente.prob(l))

            idAnt = ids
            codAnt = cods
            probAnt = probs

        return CodigoBloqueFactory.crear(idAnt, codAnt, probAnt)

    @staticmethod
    def __huffmanRec(probs: dict) -> dict:
        orden = list(probs.keys())
        l = len(orden)
        if l > 2:
            orden.sort(reverse=True, key=lambda x: probs[x])
            combinados = (orden[-2], orden[-1])
            # modifico el dict de probabilidad para pasarlo al paso siguiente
            probs[combinados[0]] = probs[combinados[0]] + probs[combinados[1]]
            del probs[combinados[1]]
            res = CodigoBloqueFactory.__huffmanRec(probs)
            codComb = res[combinados[0]]
            res[combinados[0]] = codComb + "0"
            res[combinados[1]] = codComb + "1"
        else:
            if l == 2:
                res = {orden[0]: "1", orden[1]: "0"}
            else:
                res = {orden[0]: "" }
        return res

    @staticmethod
    def huffman(fuente: FuenteDeInfo) -> CodigoBloque:
        # clono el diccionario para no destruirlo
        codigo = CodigoBloqueFactory.__huffmanRec(fuente.probs.copy())
        return CodigoBloque(fuente, codigo)

    @staticmethod
    def __shannonFanoRec(probs: dict, tope: float) -> dict:
        orden = list(probs.keys())
        orden.sort(reverse=True, key=lambda x: probs[x])
        l = len(orden)
        if l > 2:
            t, suma = 0, 0
            dif, minimo = 1, 2
            while dif < minimo:
                suma += probs[orden[t]]
                t += 1
                minimo, dif = dif, abs(tope - 2*suma)

            menoresDict = {orden[k]: probs[orden[k]] for k in range(t)}
            mayoresDict = {orden[k]: probs[orden[k]] for k in range(t, l)}
            res = {}
            resAux = CodigoBloqueFactory.__shannonFanoRec(menoresDict, suma)
            for k, v in list(resAux.items()):
                res[k] = "1" + v

            resAux = CodigoBloqueFactory.__shannonFanoRec(mayoresDict, tope - suma)
            for k, v in list(resAux.items()):
                res[k] = "0" + v
        else:
            if l == 2:
                res = {orden[0]: "1", orden[1]: "0"}
            else:
                res = {orden[0]: "" }
        return res


    @staticmethod
    def shannonFano(fuente: FuenteDeInfo) -> CodigoBloque:
        codigo = CodigoBloqueFactory.__shannonFanoRec(fuente.probs, 1)
        return CodigoBloque(fuente, codigo)



def cumpleKraft(codigo: CodigoBloque, r: int) -> bool:
    suma = 0
    for i in codigo.listaCodigos():
        suma += r**-len(i)
        if round(suma, 2) > 1:
            return False
    return True


def esCompacto(codigo: CodigoBloque) -> bool:
    for i in codigo.fuente.ids:
        if len(codigo.codigo(i)) > ceil(codigo.fuente.cantInformacion(i)):
            return False
    return True


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
            if i != j and y.startswith(x):
                return False
    return True


# fuente = FuenteDeInfo(["s1", "s2", "s3", "s4"], {
#     "s1": 0.6,
#     "s2": 0.2,
#     "s3": 0.1,
#     "s4": 0.1
# })

# fuente = FuenteDeInfoFactory.crear(
#     ["S1", "S2", "S3", "S4"], [4/10, 1/10, 3/10, 2/10])


# fuente = FuenteDeInfo(["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"], {
#     "s1": 0.40,
#     "s2": 0.20,
#     "s3": 0.15,
#     "s4": 0.10,
#     "s5": 0.06,
#     "s6": 0.04,
#     "s7": 0.03,
#     "s8": 0.02
# })

# # print(*CodigoBloqueFactory.huffman(fuente).reporte())
# print(*CodigoBloqueFactory.shannonFano(fuente).reporte())
