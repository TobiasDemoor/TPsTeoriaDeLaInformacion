from math import log2, ceil

def creaCodif(dist):
    dic = {i : ceil(-log2(dist.prob(i))) for i in dist.valores}
    sig, ant = "", 0
    for k, v in sorted(dic.items(), key = lambda x: x[1]):
        if v != ant:
            sig += "0" * (v-ant)
            ant = v
        dic[k] = sig
        sig = bin(int(sig, 2)+1)[2:].zfill(v)
    return dic

def longMedia(dist, codigo):
    res = 0
    for i in dist.valores:
        res += dist.prob(i) * len(codigo[i])
    return res

def isCompacto(dist, codigo):
    return dist.entropia() <= longMedia(dist, codigo)

def cumpleKraft(codigo: dict, r: int):
    suma = 0
    for i in codigo.items():
        suma += r**-len(i[1])
        if round(suma, 2) > 1: return False
    return True