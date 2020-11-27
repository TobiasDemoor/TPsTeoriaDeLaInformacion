from functools import cached_property
from fuentesDeInfo import FuenteDeInfo

class CodigoBloque:
    """Clase que representa un código bloque"""

    def __init__(self, fuente, codigos):
        self.fuente = fuente
        self.codigos = codigos

    def codigo(self, id) -> str:
        """Retorna el código asociado a un símbolo id"""

        return self.codigos[id]

    @cached_property
    def listaCodigos(self) -> list:
        """Retorna los códigos del código bloque en una lista"""

        return list(self.codigos.values())

    def codifica(self, mensaje: str) -> str:
        """Codifica un mensaje a con el código bloque"""

        res = ""
        for c in mensaje.lower():
            if c in self.fuente.ids:
                res += self.codigo(c)
            else:
                raise Exception(f"El simbolo {c} no existe en el CodigoBloque")
        return res
    
    @cached_property
    def rendimiento(self):
        """Calcula el rendimiento de la codificación"""
        
        return self.fuente.entropia/self.longMedia

    @cached_property
    def redundancia(self):
        """Calcula el redundancia de la codificación"""
        
        return 1 - self.rendimiento
    
    def nTasaDeCompresion(self, mensaje: str) -> float:
        """
            Calcula la tasa de compresión con un mensaje especifico, 
            codificandolo segun su codigo bloque
        """

        # multiplicamos la longitud del mensaje por 8 porque compara longitudes en bits
        return len(mensaje)*8/len(self.codifica(mensaje))

    @cached_property
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
        return (
            entropia,
            "\n\n", df,
            f"\n\nRedundancia: {self.redundancia}",
            f"\n\nRendimiento: {self.rendimiento}\n",
        )


class CodigoBloqueFactory:
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
            res[combinados[0]] = codComb + "1"
            res[combinados[1]] = codComb + "0"
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
            sumaAux = 0
            t, suma = -1, 0
            dif, minimo = 1, 2
            while dif < minimo:
                t += 1
                sumaAux = suma
                suma += probs[orden[t]]
                minimo, dif = dif, abs(tope - 2*suma)

            menoresDict = {orden[k]: probs[orden[k]] for k in range(t)}
            mayoresDict = {orden[k]: probs[orden[k]] for k in range(t, l)}
            res = {}
            resAux = CodigoBloqueFactory.__shannonFanoRec(menoresDict, sumaAux)
            for k, v in list(resAux.items()):
                res[k] = "1" + v

            resAux = CodigoBloqueFactory.__shannonFanoRec(mayoresDict, tope - sumaAux)
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



def codificaRLC(mensaje: str, legible: bool = False) -> str:
    """
        Retorna el mensaje codificado con RLC, por defecto los numeros están
        codificados dentro del caracter como un número binario. En caso de enviar
        un valor verdadero en el parametro legible los números en el mensaje codificado
        estarán en hexadecimal.
    """

    res, ant, cant = "", None, None
    parseCant = lambda x: chr(x)
    if legible:
        parseCant = lambda x: hex(x)[2:]
    for c in mensaje:
        if c != ant:
            if ant != None:
                res += parseCant(cant) + ant
            ant, cant = c, 1
        else:
            cant += 1
    if ant != None:
        res += parseCant(cant) + ant
    return res


def nTasaDeCompresion(codOriginal, codComprimido):
    """
        Calcula la tasa de compresión con un mensaje especifico, 
        codificandolo segun su codigo bloque
    """

    return len(codOriginal)/len(codComprimido) 