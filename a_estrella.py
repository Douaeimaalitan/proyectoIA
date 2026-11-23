import heapq
from red_monterrey.estacion import Estacion
from red_monterrey.conexion import Conexion
from red_monterrey.red import Red
from .heuristica import Heuristica

def a_estrella(origen : Estacion, destino : Estacion, red : Red, h : Heuristica):
    abiertos = []
    cerrados = set()
    g = {}
    g[(origen, None)] = 0
    padres = {}
    heapq.heappush(abiertos, (h.funcionH(origen, destino), (origen, None)))
    while abiertos:
        f_actual, actual = heapq.heappop(abiertos)
        if actual[0] == destino:
            camino = camino(padres, actual)
            break
        cerrados.add(actual)
        for conexion in red.conexiones[actual[0]]:
            extremo = conexion.est2
            linea = conexion.linea
            tiempo = conexion.tiempo
            vecino = (extremo, linea)
            if vecino in cerrados:
                continue

            peso = tiempo + g[actual]
            if actual[1] is not None and linea != actual[1]:
                peso = peso + red.trasbordos[linea, actual[1]]
            if vecino not in g:
                padres[vecino] = actual
                g[vecino] = peso
                heapq.heappush(abiertos, (peso + h(extremo, destino), vecino))
            elif peso >= g[vecino]:
                continue
            else:
                padres[vecino] = actual
                g[vecino] = peso
                heapq.heappush(abiertos, (peso + h(extremo, destino), vecino))       
    return camino

def camino():
    pass