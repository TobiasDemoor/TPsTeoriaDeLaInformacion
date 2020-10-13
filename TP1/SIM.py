# Módulo de simulación creado para investigación operativa
import matplotlib.pyplot as plt
from scipy import stats
from numpy import e
from math import factorial


class DistExpFactory:
    @staticmethod
    def fromProbAbs(valores, probAbs):
        """Genera un objeto Distribución experimental a partir de los valores y sus probabilidades absolutas"""

        s = 0
        probAcum = []
        for i in probAbs:
            s += i
            probAcum.append(s)
        return DistExp(valores, probAcum)

    @staticmethod
    def fromFrecuencia(valores, frecuencias):
        """Genera un objeto Distribución experimental a partir de los valores y sus frecuencias"""

        suma = sum(frecuencias)
        prob = []
        for i in frecuencias:
            prob.append(i/suma)
        return DistExpFactory.fromProbAbs(valores, prob)

    @staticmethod
    def fromMuestra(muestra):
        """Genera un objeto Distribución experimental a partir de una muestra"""

        valores = list(set(muestra))
        valores.sort()
        cant = len(muestra)
        probAcum = []
        aux = 0
        for i in valores:
            aux += muestra.count(i)/cant
            probAcum.append(aux)
        return DistExp(valores, probAcum)


class Dist:
    def __init__(self, valores):
        self.valores = valores

    def setValores(self, valores):
        self.valores = valores

    def getValores(self):
        return self.valores

    def inversa(self, prob):
        """Retorna un valor a partir de su probabilidad acumulada, debe ser definida en sub clase"""

        raise NotImplementedError()

    def prob(self, x):
        """Retorna la probabilidad de un valor, debe ser definida en sub clase"""

        raise NotImplementedError()

    def simulacion(self, rand):
        """Genera una colección de valores a partir de una lista de probabilidades"""

        res = []
        for i in rand:
            res.append(self.inversa(i))
        return res

    def distSimulacion(self, rand):
        """Genera una distribución simulada a partir de una lista de probabilidades

        Su uso es más que nada para verificar si la simulación es correcta
        """

        sim = self.simulacion(rand)
        freq = []
        for i in self.valores:
            freq.append(sim.count(i))
        return DistSimulada(self.valores, freq, sim)


class DistExp(Dist):
    """Clase distribución experimental"""

    def __init__(self, valores, probAcum):
        self.probAcum = probAcum
        super().__init__(valores)

    def setProbAcum(self, probAcum):
        self.probAcum = probAcum

    def getProbAcum(self):
        return self.probAcum

    def inversa(self, prob):
        i = 0
        while not(self.probAcum[i] >= prob):
            i += 1
        return self.valores[i]

    def prob(self, x):
        res = 0
        i = self.valores.index(x)
        if i != -1:
            if i > 0:
                res = (self.probAcum[i]-self.probAcum[i-1])
            else:
                res = self.probAcum[i]
        return res


class DistSimulada(DistExp):
    """Clase distribución simulada

    Representa una distribución simulada a partir de otra utilizando método Montecarlo
    """

    def __init__(self, valores, frecuencias, muestra):
        self.muestra = muestra
        suma = sum(frecuencias)
        aux = 0
        prob = []
        for i in frecuencias:
            aux += i/suma
            prob.append(aux)
        super().__init__(valores, prob)

    def getMuestra(self):
        return self.muestra


class DistTeoricaDiscreta(Dist):
    def __init__(self, funcion, techo=0, piso=0):
        self.funcion = funcion
        self.piso = piso
        if techo == None:
            # si techo es None significa que está definida [piso;infinito)
            i = 0
            while funcion(i) > 1e-4:
                i += 1
            techo = i
        self.techo = techo
        super().__init__(range(piso, techo+1))

    def setPiso(self, piso):
        self.piso = piso
        super().setValores(range(piso, self.techo+1))

    def setTecho(self, techo):
        self.techo = techo
        super().setValores(range(self.piso, techo+1))

    def getProbAcum(self):
        prob = []
        aux = 0
        for i in self.valores:
            aux += self.funcion(i)
            prob.append(aux)
        return prob

    def inversa(self, prob):
        i = 0
        acum = self.funcion(i)
        while not(acum > prob):
            i += 1
            acum += self.funcion(i)
        return i

    def prob(self, x):
        return self.funcion(x)


def simulacion(rand, inversa):
    res = []
    for i in rand:
        res.append(inversa(i))
    return res


def poisson(mu, k):
    return (e**(-mu) * mu**k)/factorial(k)


def exponInv(lam, prob):
    return stats.expon.ppf(prob, 0, lam)


def normInv(mu, sigma, prob):
    return stats.norm.ppf(prob)*sigma+mu


def regr(x, y):
    m, b, r, _ = stats.linregress(x, y)
    plt.plot(x, y, 'o')
    ajust = []
    for i in x:
        ajust.append(b + m*i)
    plt.plot(x, ajust, 'r')
    return m, b, r
