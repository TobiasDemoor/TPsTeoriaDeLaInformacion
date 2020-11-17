from math import log2

class Canal:
    def __init__(self, simbIn: set, simbOut: set, mat: dict, probIn):
        self.simbIn = simbIn
        self.simbOut = simbOut
        self.mat = mat
        self.probIn = probIn
        
    @property
    def aPriori(self) -> dict:
        return self.probIn

    @property
    def aPosteriori(self) -> dict:
        try:
            return self.__aPosteriori
        except ValueError:
            simbIn = self.simbIn
            simbOut = self.simbOut
            probIn = self.probIn
            mat = self.mat

            prob = {}
            for i in simbIn:
                prob[i] = {}
                for j in simbOut:
                    prob[i][j] = mat[i][j] * probIn[i] / sum(
                        [mat[i][j] * probIn[i] for i in simbIn]
                    )

            self.__aPosteriori = prob
            return self.__aPosteriori

    @property
    def entropiaAPriori(self) -> float:
        entropia = 0
        for i in self.simbIn:
            if self.probIn[i] != 0:
                entropia += -self.purobIn[i] * log2(self.probIn[i])
        return entropia

    def entropiaAPosteriori(self, j: str) -> float:
        entropia = 0
        for i in self.simbIn:
            entropia += -self.mat[i][j] * log2(self.mat[i][j]) 
        return entropia
    
    
    def probSimultanea(self, a: str, b: str) -> float:
        return self.mat[a][b] * self.probIn[a]


class CanalFactory:
    @staticmethod
    def fromMat(simbIn: list, simbOut: list, mat: list, probIn: list) -> Canal:
        simbInSet = sorted(set(simbIn))
        simbOutSet = sorted(set(simbOut))

        matC = {
            si: {
                sj: mat[i][j] for j, sj in enumerate(simbOutSet)
            } for i, si in enumerate(simbInSet)
        }
        probInC = {si: probIn[i] for i, si in enumerate(simbInSet)}

        return Canal(simbInSet, simbOutSet, matC, probInC)

    @staticmethod
    def fromMuestras(entrada: str, salida: str) -> Canal:
        simbIn = sorted(set(entrada))
        simbOut = sorted(set(salida))

        suma = len(entrada)
        probIn = {i: entrada.count(i)/suma for i in simbIn}

        sumas = {i: 0 for i in simbIn}
        mat = {i: {j: 0 for j in simbOut} for i in simbIn}

        for ind, j in enumerate(salida):
            i = entrada[ind]
            mat[i][j] += 1
            sumas[i] += 1

        for i in simbIn:
            if sumas[i] != 0:
                for j in simbOut:
                    mat[i][j] /= sumas[i]

        return Canal(simbIn, simbOut, mat, probIn)
