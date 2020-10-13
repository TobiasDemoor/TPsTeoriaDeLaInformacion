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

def esCodBloque(aCodigo: list, codigoBloque: list) -> bool:
    bloqueaux = codigoBloque[:]
    aaux = aCodigo[:]
    longmax = len(max(bloqueaux, key=len))
    it = 0
    while len(bloqueaux) > 0 and it < longmax:
        for i in aaux:
            while i in bloqueaux:
                bloqueaux.remove(i)
        lista = []
        for i in aaux:
            for j in aCodigo:
                lista.append(i + j)
        aaux = lista
        it += 1
    return len(bloqueaux) == 0

def esNoSingular(codigoBloque: list) -> bool:
    return len(set(codigoBloque)) == len(codigoBloque)
        
def esInstantaneo(codigoBloque: list) -> bool:
    for i, x in enumerate(codigoBloque):
        for j, y in enumerate(codigoBloque):
            if y.find(x) == 0 and i != j:
                return False
    return True
    # version fea
    # i, cumple = 0, True
    # largo = len(codigoBloque)
    # while i < largo and cumple:
    #     x, j = codigoBloque[i], 0
    #     while j < largo and cumple:
    #         y = codigoBloque[j]
    #         if y.find(x) == 0 and i !=j:
    #             cumple = False
    #         j += 1
    #     x += 1
    # return cumple
