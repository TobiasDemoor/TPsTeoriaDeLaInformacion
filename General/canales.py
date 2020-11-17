from math import log2

class Canal:
    def __init__(self, simbIn: set, simbOut: set, mat: dict, probIn):
        self.simbIn = simbIn
        self.simbOut = simbOut
        self.mat = mat
        self.probIn = probIn
        
    @property
    def probOut(self) -> dict:
        try:
            return self.__probOut
        except AttributeError:
            self.__probOut = {
                j: sum(
                    [ self.mat[i][j] * self.probIn[i] for i in self.simbIn ]
                ) for j in self.simbOut
            }
            return self.__probOut

    @property
    def aPriori(self) -> dict:
        return self.probIn

    @property
    def aPosteriori(self) -> dict:
        try:
            return self.__aPosteriori
        except AttributeError:
            simbIn = self.simbIn
            simbOut = self.simbOut
            probIn = self.probIn
            probOut = self.probOut
            mat = self.mat

            self.__aPosteriori = {
                i: {
                    j: mat[i][j] * probIn[i] / probOut[j] for j in simbOut
                } for i in simbIn
            }
        
            return self.__aPosteriori

    @property
    def entropiaAPriori(self) -> float:
        entropia = 0
        for i in self.simbIn:
            if self.probIn[i] != 0:
                entropia += -self.probIn[i] * log2(self.probIn[i])
        return entropia

    def entropiaAPosteriori(self, j: str) -> float:
        entropia = 0
        for i in self.simbIn:
            if self.mat[i][j] != 0:
                entropia += -self.mat[i][j] * log2(self.mat[i][j]) 
        return entropia
    
    @property
    def entropiasAPosteriori(self) -> dict:
        return {j: self.entropiaAPosteriori(j) for j in self.simbOut}
    
    
    def probSimultanea(self, a: str, b: str) -> float:
        return self.mat[a][b] * self.probIn[a]
    
    
    @property
    def probSimultaneas(self) -> dict:
        return {i: {j: self.probSimultanea(i,j) for j in self.simbOut} for i in self.simbIn}
    


class CanalFactory:
    @staticmethod
    def fromMat(simbIn: list, simbOut: list, mat: list, probIn: list) -> Canal:
        simbInSet = set(simbIn)
        simbOutSet = set(simbOut)

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