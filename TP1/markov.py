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
            B = np.zeros_like(A[0])
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
