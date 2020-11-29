from graphviz import Digraph
from fuentesDeInfo import FuenteDeInfoFactory

def huffmanGraph(probs: dict, dot: Digraph):
    if len(probs) > 1:
        orden = sorted(probs.keys(), reverse=True, key= lambda x: probs[x])
        combs = (orden[-2], orden[-1])
        comb = ','.join(combs)
        pcomb = sum([probs[x] for x in combs])
        dot.node(f"{comb}\n{pcomb:.2f}", label=f"{pcomb:.2f}")
        dot.edge(f"{combs[0]}\n{probs[combs[0]]:.2f}", f"{comb}\n{pcomb:.2f}", '1')
        dot.edge(f"{combs[1]}\n{probs[combs[1]]:.2f}", f"{comb}\n{pcomb:.2f}", '0')
        del probs[combs[0]]
        del probs[combs[1]]
        probs[comb] = pcomb
        huffmanGraph(probs, dot)


def graficaHuff():
    arch = open("mdp-espanol.txt", "r", encoding="utf-8")
    mensaje = arch.read()
    fuente = FuenteDeInfoFactory.fromMuestra(mensaje)
    dot = Digraph(node_attr={'shape': 'circle'}, edge_attr={'dir': 'none'})
    huffmanGraph(fuente.probs.copy(), dot)
    dot.render("huffman", format="png")

def shannonGraph(probs: dict, dot: Digraph, tope: int, padre: str):
    l = len(probs)
    if l > 1:
        orden = sorted(probs.keys(), reverse=True, key= lambda x: probs[x])
        sumaAux = 0
        t, suma = -1, 0
        dif, minimo = 1, 2
        while dif < minimo: 
            t += 1
            sumaAux = suma
            suma += probs[orden[t]]
            minimo, dif = dif, abs(tope - 2*suma)

        menoresDict = {orden[k]: probs[orden[k]] for k in range(t)}
        mayoresDict = {orden[k]: probs[orden[k]] for k in range(t, l)}

        nodoMenor = f'{menoresDict.keys()}'
        nodoMayor = f'{mayoresDict.keys()}'

        if len(menoresDict) == 1:
            dot.node(nodoMenor, label=f"{orden[t-1]}\n{sumaAux:.2f}")
        else:
            dot.node(nodoMenor, label=f"{sumaAux:.2f}")

        if len(mayoresDict) == 1:
            dot.node(nodoMayor, label=f"{orden[t]}\n{(tope - sumaAux):.2f}")
        else:
            dot.node(nodoMayor, label=f"{(tope - sumaAux):.2f}")

        dot.edge(padre, nodoMenor, '1')
        dot.edge(padre, nodoMayor, '0')

        shannonGraph(menoresDict, dot, sumaAux, nodoMenor)
        shannonGraph(mayoresDict, dot, tope - sumaAux, nodoMayor)

def graficaShann():
    arch = open("mdp-espanol.txt", "r", encoding="utf-8")
    mensaje = arch.read()
    fuente = FuenteDeInfoFactory.fromMuestra(mensaje)
    dot = Digraph(node_attr={'shape': 'circle'}, edge_attr={'dir': 'none'})
    dot.node('padre', label="1.00")
    shannonGraph(fuente.probs.copy(), dot, 1.0, 'padre')
    dot.render("shann", format="png")

graficaShann()