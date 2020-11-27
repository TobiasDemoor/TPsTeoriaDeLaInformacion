from functools import cached_property
from math import log2
import pandas as pd

class Canal:
    def __init__(self, simbIn: list, simbOut: list, mat: dict, probIn):
        self.simbIn = simbIn
        self.simbOut = simbOut
        self.mat = mat
        self.probIn = probIn
        
    @cached_property
    def probOut(self) -> dict:
        """Calcula la probabilidad de salida"""

        return {
            j: sum(
                [ self.mat[i][j] * self.probIn[i] for i in self.simbIn ]
            ) for j in self.simbOut
        }

    @cached_property
    def aPriori(self) -> dict:
        """Devuelve la probabilidad de entrada"""

        return self.probIn

    @cached_property
    def aPosteriori(self) -> dict:
        """Calcula la matriz de probabilidades a posteriori (ai/bi)"""

        simbIn = self.simbIn
        simbOut = self.simbOut
        probIn = self.probIn
        probOut = self.probOut
        mat = self.mat

        return {
            i: {
                j: mat[i][j] * probIn[i] / probOut[j] for j in simbOut
            } for i in simbIn
        }

    @cached_property
    def entropiaAPriori(self) -> float:
        """Calcula la entropía a priori"""

        entropia = 0
        for i in self.simbIn:
            if self.probIn[i] != 0:
                entropia += -self.probIn[i] * log2(self.probIn[i])
        return entropia

    def entropiaAPosteriori(self, j: str) -> float:
        """Calcula la entropía a posteriori habiendo salido el simbolo j"""

        entropia = 0
        probAPost = self.aPosteriori
        for i in self.simbIn:
            if probAPost[i][j] != 0:
                entropia += -probAPost[i][j] * log2(probAPost[i][j]) 
        return entropia
    
    @cached_property
    def entropiasAPosteriori(self) -> dict:
        """Calcula las entropías a posteriori"""

        return {
            j: self.entropiaAPosteriori(j) for j in self.simbOut
        }
    
    def probSimultanea(self, a: str, b: str) -> float:
        """Calcula probabilidad mutua P(a, b)"""

        return self.mat[a][b] * self.probIn[a]
    
    @cached_property
    def probSimultaneas(self) -> dict:
        """Calcula la equivocación del canal"""
        
        return {
            i: {
                j: self.probSimultanea(i,j) for j in self.simbOut
            } for i in self.simbIn
        }

    @cached_property
    def equivocacion(self) -> float:
        """Calcula la equivocación del canal"""

        probSim = self.probSimultaneas
        res = 0
        for i in self.simbIn:
            for j in self.simbOut:
                if probSim[i][j] != 0:
                    res += probSim[i][j] * -log2(probSim[i][j])
        return res

    @cached_property
    def canalInverso(self) -> object:
        """
            Retorna un canal donde la matriz probabilidades a posteriori
            y las probabilidades  actual de salida serán la matriz de probabilidades 
            y las probabilidades a priori respectivamente.
        """    

        mat = { j: { i: self.aPosteriori[i][j] for i in self.simbIn } for j in self.simbOut }
        return Canal(self.probOut, self.probIn, mat, self.probOut)

    @cached_property
    def infMutua(self) -> float:
        """Devuelve la información mutua I(A, B)"""

        probSim = self.probSimultaneas
        res = 0
        for i in self.simbIn:
            for j in self.simbOut:
                if probSim[i][j] != 0:
                    res += probSim[i][j] * log2(
                        probSim[i][j] / ( self.aPriori[i] * self.probOut[j] )
                    )
        return res
    
    @cached_property
    def infMutuaInversa(self) -> float:
        """Devuelve la información mutua I(B, A)"""

        return self.canalInverso.infMutua

    @cached_property
    def entropiaB(self) -> float:
        return self.canalInverso.entropiaAPriori

    def reportes(self) -> tuple:
        probOut = pd.DataFrame({"P(b)":self.probOut}).transpose()
        probOut = probOut[self.simbOut]

        probAPriori = pd.DataFrame({"P(a):":self.aPriori}).transpose()
        probAPriori = probAPriori[self.simbIn]

        probAPost = pd.DataFrame(self.aPosteriori).transpose()
        probAPost = probAPost[self.simbOut]
        probAPost.reindex(self.simbIn)

        probSimultaneas = pd.DataFrame(self.probSimultaneas).transpose()
        probSimultaneas = probSimultaneas[self.simbOut]
        probSimultaneas.reindex(self.simbIn)

        entropiaPost = pd.DataFrame({"H(A/bj)": self.entropiasAPosteriori}).transpose()
        entropiaPost = entropiaPost[self.simbOut]

        return (
            "\n\nProbabilidades de salida\n", probOut, "\n",
            "\n\nProbabilidades a priori\n", probAPriori, "\n",
            "\n\nProbabilidades a posteriori\n", probAPost, "\n",
            "\n\nProbabilidades simultaneas\n", probSimultaneas, "\n",
            "\n\nEntropía a posteriori\n", entropiaPost, "\n",
            f"\n\nEntropía a priori = H(A) = {self.entropiaAPriori}",
            f"\n\nEquivocación = H(A/B) = {self.equivocacion} (RUIDO)",
            f"\n\nH(B) = {self.entropiaB}",
            f"\n\nInformación mutua = I(A,B) = {self.infMutua}",
            f"\n\nI(A,B) = {self.infMutua} ≥ 0",
            f"\n\nI(B,A) = {self.infMutuaInversa} = I(A,B) = {self.infMutua}"
        )
        
        

class CanalFactory:
    @staticmethod
    def fromMat(simbIn: list, simbOut: list, mat: list, probIn: list) -> Canal:
        """Retorna un objeto Canal a partir de la matriz de probabilidades"""
        matC = {
            si: {
                sj: mat[i][j] for j, sj in enumerate(simbOut)
            } for i, si in enumerate(simbIn)
        }
        probInC = {si: probIn[i] for i, si in enumerate(simbIn)}

        return Canal(simbIn, simbOut, matC, probInC)
