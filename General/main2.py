#################### Primera Parte ####################
from fuentesDeInfo import FuenteDeInfo, FuenteDeInfoFactory
from codificacion import CodigoBloque, CodigoBloqueFactory, codificaRLC, decoRLC
"""
    Hay que codificar ambas, para Huff y S-F hay que escribir la tabla de codigo bloque.
    Para RLC hay que mostrar el código comprimido.
"""


# Fuente 1
arch = open("mdp-espanol.txt", "r", encoding="utf-8")
mensaje = arch.read()
fuente = FuenteDeInfoFactory.fromMuestra(mensaje)
huff1 = CodigoBloqueFactory.huffman(fuente)
shan1 = CodigoBloqueFactory.shannonFano(fuente)
rlc1 = codificaRLC(mensaje)

# arch.close()
# arch = open("res.txt", "w", encoding="utf-8")
# arch.write("".join([chr(i) for i in rlc1]))
print(*huff1.reporte())
print(*shan1.reporte())
arch.close()

# Fuente 2
arch = open("mdp-portugues.txt", "r", encoding="utf-8")
mensaje = arch.read()
fuente = FuenteDeInfoFactory.fromMuestra(mensaje)
huff2 = CodigoBloqueFactory.huffman(fuente)
shan2 = CodigoBloqueFactory.shannonFano(fuente)
rlc2 = codificaRLC(mensaje)

# arch.close()
# arch = open("res2.txt", "w", encoding="utf-8")
# arch.write("".join([chr(i) for i in rlc1]))
print(*huff2.reporte())
print(*shan2.reporte())
arch.close()

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
canal1 = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

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
canal2 = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

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
canal3 = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)
