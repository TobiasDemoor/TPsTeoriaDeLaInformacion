import numpy as np
from math import log2
from graphviz import Digraph

class FuenteDeMarkov:
    """Clase que representa una fuente de Markov de memoria 1"""

    def __init__(self, ids, mat):
        self.ids = ids
        self.mat = mat
    
    @property
    def vectorEstacionario(self) -> np.ndarray:
        """Vector estacionario de la fuente"""

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
        """Calcula la entropia de la fuente"""
        ent = 0
        v = self.vectorEstacionario
        for j, val in enumerate(v):
            for i in range(len(v)):
                if self.mat[i][j] != 0:
                    ent += val * self.mat[i][j] * -log2(self.mat[i][j])
        return ent

    @property
    def grafo(self) -> Digraph:
        """Grafo que representa la fuente"""
        try:
            return self.__grafo
        except AttributeError:
            dot = Digraph(node_attr={'shape': 'circle'})
            for i, valO in enumerate(self.ids):
                for j, valD in enumerate(self.ids):
                    if self.mat[i][j] != 0:
                        dot.edge(valO, valD, str(round(self.mat[i][j], 5)))
            self.__grafo = dot
            return self.__grafo
