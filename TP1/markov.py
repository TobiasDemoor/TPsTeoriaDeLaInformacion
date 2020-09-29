import numpy as np
from math import log2


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
            if np.all(A[-1] == 0.0):
                A[-1] = np.ones_like(A[0])
                B[-1] = 1

            self.__vectorEstacionario = np.linalg.solve(A, B)
            return self.__vectorEstacionario

    def entropia(self) -> float:
        ent = 0
        v = self.vectorEstacionario
        for j, val in enumerate(v):
            for i in range(len(v)):
                ent += val * self.mat[i][j] * -log2(self.mat[i][j])
        return ent
