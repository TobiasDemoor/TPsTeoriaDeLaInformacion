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
        """Retorna la probabilidad de salida P(bj)"""

        return {
            bj: sum(
                [ self.mat[ai][bj] * self.probIn[ai] for ai in self.simbIn ]
            ) for bj in self.simbOut
        }

    @cached_property
    def aPriori(self) -> dict:
        """Retorna la probabilidad aPriori osea la probabilidad de entrada P(ai)"""

        return self.probIn

    @cached_property
    def aPosteriori(self) -> dict:
        """Retorna la matriz de probabilidades a posteriori P(ai/bj)"""

        return {
            ai: {
                bj: self.mat[ai][bj] * self.probIn[ai] / self.probOut[bj]
                    for bj in self.simbOut
            } for ai in self.simbIn
        }

    @cached_property
    def entropiaAPriori(self) -> float:
        """Retorna la entropía a priori H(A)"""

        entropia = 0
        for ai in self.simbIn:
            if self.probIn[ai] != 0:
                entropia += -self.probIn[ai] * log2(self.probIn[ai])

        return entropia

    def entropiaAPosteriori(self, bj: str) -> float:
        """Retorna la entropía a posteriori habiendo salido el simbolo bj H(A/bj)"""

        entropia = 0
        for ai in self.simbIn:
            if self.aPosteriori[ai][bj] != 0:
                entropia += -self.aPosteriori[ai][bj] * log2(self.aPosteriori[ai][bj]) 
        return entropia
    
    @cached_property
    def entropiasAPosteriori(self) -> dict:
        """Retorna las entropías a posteriori H(A/bj) para todo bj"""

        return {
            bj: self.entropiaAPosteriori(bj) for bj in self.simbOut
        }
    
    def probSimultanea(self, ai: str, bj: str) -> float:
        """Retorna probabilidad simultanea P(ai, bj)"""

        return self.mat[ai][bj] * self.probIn[ai]
    
    @cached_property
    def probSimultaneas(self) -> dict:
        """Retorna todas las probabilidades simultaneas P(ai, bj) para todo par ai, bj"""
        
        return {
            ai: {
                bj: self.probSimultanea(ai,bj) for bj in self.simbOut
            } for ai in self.simbIn
        }

    @cached_property
    def equivocacion(self) -> float:
        """Retorna la equivocación del canal"""

        res = 0
        for ai in self.simbIn:
            for bj in self.simbOut:
                if self.probSimultaneas[ai][bj] != 0:
                    res += self.probSimultaneas[ai][bj] * -log2(self.aPosteriori[ai][bj])
        return res

    @cached_property
    def infMutua(self) -> float:
        """Retorna la información mutua I(A, B)"""

        res = 0
        for ai in self.simbIn:
            for bj in self.simbOut:
                if self.probSimultaneas[ai][bj] != 0:
                    res += self.probSimultaneas[ai][bj] * log2(
                        self.probSimultaneas[ai][bj] / ( self.probIn[ai] * self.probOut[bj] )
                    )
        return res
    
    @cached_property
    def canalInverso(self) -> object:
        """
            Retorna un canal donde la matriz probabilidades a posteriori
            y las probabilidades  actual de salida serán la matriz de probabilidades 
            y las probabilidades a priori respectivamente.
        """    

        mat = {
            bj: {
                ai: self.aPosteriori[ai][bj] for ai in self.simbIn
            } for bj in self.simbOut
        }
        return Canal(self.probOut, self.probIn, mat, self.probOut)

    @cached_property
    def infMutuaInversa(self) -> float:
        """Retorna la información mutua del canal inverso I(B, A)"""

        return self.canalInverso.infMutua

    def reporte(self) -> tuple:
        probAPriori = pd.DataFrame({"P(ai):":self.aPriori}).transpose()
        probAPriori = probAPriori[self.simbIn]

        probAPost = pd.DataFrame(self.aPosteriori).transpose()
        probAPost = probAPost[self.simbOut]
        probAPost.reindex(self.simbIn)

        entropiaPost = pd.DataFrame({"H(A/bj)": self.entropiasAPosteriori}).transpose()
        entropiaPost = entropiaPost[self.simbOut]

        return (
            "\n\nProbabilidades a priori\n", probAPriori, "\n",
            "\n\nProbabilidades a posteriori P(ai/bj)\n", probAPost, "\n",
            "\n\nEntropía a posteriori\n", entropiaPost, "\n",
            f"\n\nEntropía a priori = H(A) = {self.entropiaAPriori}",
            f"\n\nEquivocación = H(A/B) = {self.equivocacion} (RUIDO)",
            f"\n\nInformación mutua = I(A,B) = {self.infMutua} ≥ 0",
            f"\n\nI(B,A) = {self.infMutuaInversa} = I(A,B) = {self.infMutua}"
        )
        
        

class CanalFactory:
    @staticmethod
    def fromMat(simbIn: list, simbOut: list, mat: list, probIn: list) -> Canal:
        """Retorna un objeto Canal a partir de la matriz de probabilidades"""
        matC = {
            ai: {
                bj: mat[i][j] for j, bj in enumerate(simbOut)
            } for i, ai in enumerate(simbIn)
        }
        probInC = {ai: probIn[i] for i, ai in enumerate(simbIn)}

        return Canal(simbIn, simbOut, matC, probInC)
