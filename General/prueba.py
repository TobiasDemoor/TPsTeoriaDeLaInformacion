from canales import Canal, CanalFactory
import pandas as pd

simbIn = ["0", "1"]
simbOut = ["0", "*", "1"]
probIn = [0.25, 0.75]
mat = [
    [0.5, 0.5, 0.0],
    [0.0, 1/3, 2/3]
]

# simbOut = ["0", "1", "2"]
# probIn = [0.5, 0.5]
# mat = [
#     [0.5, 0.0, 0.5],
#     [0.0, 1.0, 0.0]
# ]
canal = CanalFactory.fromMat(simbIn, simbOut, mat, probIn)

print(*canal.reportes())