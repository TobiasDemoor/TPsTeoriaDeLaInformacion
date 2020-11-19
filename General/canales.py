from math import log2
import pandas as pd

class Canal:
    def __init__(self, simbIn: list, simbOut: list, mat: dict, probIn):
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

    def reportes(self) -> tuple:
        probOut = pd.DataFrame({"P(i)":self.probOut}).transpose()
        probOut = probOut[self.simbOut]

        probAPriori = pd.DataFrame({"P(i):":self.aPriori}).transpose()
        probAPriori = probAPriori[self.simbIn]

        probAPost = pd.DataFrame(self.aPosteriori).transpose()
        probAPost = probAPost[self.simbOut]
        probAPost.reindex(self.simbIn)

        probSimultaneas = pd.DataFrame(self.probSimultaneas).transpose()
        probSimultaneas = probSimultaneas[self.simbOut]
        probSimultaneas.reindex(self.simbIn)
        
        entropiaPriori = f"H(S) = {self.entropiaAPriori}"

        entropiaPost = pd.DataFrame({"H(S)": self.entropiasAPosteriori}).transpose()
        entropiaPost = entropiaPost[self.simbOut]

        return (
            "\nProbabilidades de salida\n", probOut,
            "\n\n",
            "\nProbabilidades a priori\n", probAPriori,
            "\n\n",
            "\nProbabilidades a posteriori\n", probAPost,
            "\n\n",
            "\nProbabilidades simultaneas\n", probSimultaneas,
            "\n\n",
            "\nEntropía a priori\n", entropiaPriori,
            "\n\n",
            "\nEntropía a posteriori\n", entropiaPost
            )
        
        
    


class CanalFactory:
    @staticmethod
    def fromMat(simbIn: list, simbOut: list, mat: list, probIn: list) -> Canal:

        matC = {
            si: {
                sj: mat[i][j] for j, sj in enumerate(simbOut)
            } for i, si in enumerate(simbIn)
        }
        probInC = {si: probIn[i] for i, si in enumerate(simbIn)}

        return Canal(simbIn, simbOut, matC, probInC)

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


simbIn = ["A1", "A2", "A3"]
simbOut = ["b1", "b2", "b3", "b4"]
mat = [
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0, 0.5],
    [0.5, 0, 0.5, 0]
]
probIn = [0.25, 0.25, 0.5]
C1 = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

print(*C1.reportes())