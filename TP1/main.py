import random
import math 
import pandas
from TI import Dist, DistExp, DistExpFactory, DistSimulada, DistTeoricaDiscreta

d = DistExpFactory.fromMuestra([0,1,2,3])
# print(d.cantInformacion(1))
print(d.entropia())
print(d.reporte())