from functools import cached_property
import numpy as np
from math import log2
from graphviz import Digraph

class FuenteDeMarkov:
    """Clase que representa una fuente de Markov de memoria 1"""

    def __init__(self, ids, mat):
        self.ids = ids
        self.mat = mat
    
    @cached_property
    def vectorEstacionario(self) -> np.ndarray:
        """Vector estacionario de la fuente"""

        rango = len(self.mat)
        A = np.array(self.mat) - np.identity(rango)
        B = np.zeros_like(A[0])
        A[-1] = np.ones_like(A[0])
        B[-1] = 1
        return np.linalg.solve(A, B)    

    @cached_property
    def entropia(self) -> float:
        """Calcula la entropia de la fuente"""
        ent = 0
        v = self.vectorEstacionario
        for j, val in enumerate(v):
            for i in range(len(v)):
                if self.mat[i][j] != 0:
                    ent += val * self.mat[i][j] * -log2(self.mat[i][j])
        return ent

    @cached_property
    def grafo(self) -> Digraph:
        """Grafo que representa la fuente"""
        
        dot = Digraph(node_attr={'shape': 'circle'})
        for j, valO in enumerate(self.ids):
            for i, valD in enumerate(self.ids):
                if self.mat[i][j] != 0:
                    dot.edge(valO, valD, str(round(self.mat[j][i], 5)))
        return dot
