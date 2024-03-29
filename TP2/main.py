#################### Primera Parte ####################
from fuentesDeInfo import FuenteDeInfo, FuenteDeInfoFactory
from codificacion import CodigoBloque, CodigoBloqueFactory, codificaRLC, nTasaDeCompresion

# habilita que se muestren todas las lineas de las tablas en la consola
import pandas
pandas.set_option('display.max_rows', None)

"""
    Hay que codificar ambas, para Huff y S-F hay que escribir la tabla de codigo bloque.
    Para RLC hay que mostrar el código comprimido.
"""

# Fuente 1
arch = open("mdp-espanol.txt", "r", encoding="utf-8")
mensaje = arch.read()
fuente: FuenteDeInfo = FuenteDeInfoFactory.fromMuestra(mensaje)
huff1: CodigoBloque = CodigoBloqueFactory.huffman(fuente)
shan1: CodigoBloque = CodigoBloqueFactory.shannonFano(fuente)
arch.close()

rlc1 = codificaRLC(mensaje, True)
# se escribe el resultado en el archivo rlc1.txt
arch = open("rlc1.txt", "w", encoding="utf-8")
arch.write(rlc1)
arch.close()

print("\n\n------------ESPAÑOL------------")
print("\nRLC")
print(f"Tasa de compresion: {nTasaDeCompresion(mensaje, rlc1):.2f}:1")
print("\n\nHUFFMAN")
print(*huff1.reporte())
print(f"Tasa de compresion: {huff1.nTasaDeCompresion(mensaje):.2f}:1")
print("\n\nSHANNON-FANO")
print(*shan1.reporte())
print(f"Tasa de compresion: {shan1.nTasaDeCompresion(mensaje):.2f}:1")


# Fuente 2
arch = open("mdp-portugues.txt", "r", encoding="utf-8")
mensaje = arch.read()
fuente: FuenteDeInfo = FuenteDeInfoFactory.fromMuestra(mensaje)
huff2: CodigoBloque = CodigoBloqueFactory.huffman(fuente)
shan2: CodigoBloque = CodigoBloqueFactory.shannonFano(fuente)
arch.close()

rlc2 = codificaRLC(mensaje, True)
# se escribe el resultado en el archivo rlc2.txt
arch = open("rlc2.txt", "w", encoding="utf-8")  
arch.write(rlc2)
arch.close()

print("\n\n------------PORTUGUES------------")
print("\nRLC")
print(f"Tasa de compresion: {nTasaDeCompresion(mensaje, rlc2):.2f}:1")
print("\n\nHUFFMAN")
print(*huff2.reporte())
print(f"Tasa de compresion: {huff2.nTasaDeCompresion(mensaje):.2f}:1")
print("\n\nSHANNON-FANO")
print(*shan2.reporte())
print(f"Tasa de compresion: {shan2.nTasaDeCompresion(mensaje):.2f}:1")


#################### Segunda Parte ####################
from canales import Canal, CanalFactory

# Canal 1
print("\n\n------------ Canal 1 ------------")

simbIn = ["A1", "A2"]
simbOut = ["B1", "B2", "B3", "B4", "B5"]
probIn = [0.2, 0.8]
mat = [
    [0.2, 0.2, 0.2, 0.2, 0.2],
    [0.9, 0.1, 0.0, 0.0, 0.0]
]
canal1: Canal = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

print(*canal1.reporte())

# Canal 2
print("\n\n------------ Canal 2 ------------")

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
canal2: Canal = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

print(*canal2.reporte())

# Canal 3
print("\n\n------------ Canal 3 ------------")

simbIn = ["A1", "A2", "A3", "A4"]
simbOut = ["B1", "B2", "B3"]
probIn = [0.1, 0.1, 0.4, 0.4]
mat = [
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 0.0],
    [0.0, 0.5, 0.5],
    [1.0, 0.0, 0.0]
]
canal3: Canal = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

print(*canal3.reporte())
