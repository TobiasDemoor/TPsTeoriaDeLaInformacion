import numpy as np
from math import log2
from graphviz import Digraph

class FuenteDeMarkov:
    def __init__(self, valores, mat):
        self.valores = valores
        self.mat = mat
    
    @property
    def vectorEstacionario(self) -> np.ndarray:
        try:
            return self.__vectorEstacionario
        except AttributeError:
            rango = len(self.mat)
            A = np.array(self.mat) - np.identity(rango)
            for j in range(rango-1):
                imax = j
                for i in range(j+1,rango):
                    if abs(A[i][j]) > abs(A[imax][j]):
                        imax = i
                if A[imax][j] != 0:
                    A[j], A[imax] = A[imax], A[j]
                else:
                    print("F")
                    break
                for i in range(j+1, rango):
                    A[i][j+1:] -= A[j][j+1:]*A[i][j]/A[j][j]
                    A[i][j] = 0.0
            
            B = np.zeros_like(A[0])
            if sum(map(abs, A[-1])) < 1e-10:
                A[-1] = np.ones_like(A[0])
                B[-1] = 1

            self.__vectorEstacionario = np.linalg.solve(A, B)
            return self.__vectorEstacionario

    def entropia(self) -> float:
        ent = 0
        v = self.vectorEstacionario
        for j, val in enumerate(v):
            for i in range(len(v)):
                if self.mat[i][j] != 0:
                    ent += val * self.mat[i][j] * -log2(self.mat[i][j])
        return ent

    def generaSimbolos(self, rnd):
        j = 0 #TODO: definir el primer simbolo a partir de las probabilidades totales que no tenemos
        simbolos = []
        for k in rnd():
            acum = mat[0][j]
            i = 0
            while(acum <= k and i < len(self.mat)):
                i += 1
                acum += self.mat[i][j]
            simbolos.append(self.valores[i])
        return simbolos

    @property
    def grafo(self):
        try:
            return self.__grafo
        except AttributeError:
            dot = Digraph(node_attr={'shape': 'circle'})
            for i, valO in enumerate(self.valores):
                for j, valD in enumerate(self.valores):
                    if self.mat[i][j] != 0:
                        dot.edge(valO, valD, str(round(self.mat[i][j], 5)))
            self.__grafo = dot
            return self.__grafo
