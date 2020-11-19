#################### Primera Parte ####################
from codificacion import CodigoBloque, CodigoBloqueFactory, codificaRLC, decoRLC
# Fuente 1
arch = open("mdp-espanol.txt", "r", encoding="utf-8")

# Fuente 2
arch = open("mdp-portugues.txt", "r", encoding="utf-8")

#################### Segunda Parte ####################
from canales import Canal, CanalFactory
# Canal 1
simbIn = ["A1", "A2"]
simbOut = ["B1", "B2", "B3", "B4", "B5"]
probIn = [0.2, 0.2]
mat = [
    [0.2, 0.2, 0.2, 0.2, 0.2],
    [0.9, 0.1, 0.0, 0.0, 0.0]
]
canal = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

# Canal 2
simbIn = ["A1", "A2", "A3", "A4", "A5"]
simbOut = ["B1", "B2", "B3", "B4", "B5"]
probIn = [0.2, 0.1, 0.3, 0.1, 0.3]
mat = [
    [0.3, 0.0, 0.3, 0.1, 0.3],
    [0.2, 0.0, 0.2, 0.2, 0.4],
    [0.1, 0.2, 0.2, 0.4, 0.1],
    [0.5, 0.4, 0.1, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0]
]
canal = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

# Canal 3
simbIn = ["A1", "A2", "A3", "A4"]
simbOut = ["B1", "B2", "B3"]
probIn = [0.1, 0.1, 0.4, 0.4]
mat = [
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 0.0],
    [0.0, 0.5, 0.5],
    [1.0, 0.0, 0.0]
]
canal = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)
