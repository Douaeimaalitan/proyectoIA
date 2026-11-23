import heapq
from itertools import count
from red_monterrey.estacion import Estacion
from red_monterrey.conexion import Conexion
from red_monterrey.red import Red
from heuristica import Heuristica

def a_estrella(origen : Estacion, destino : Estacion, red : Red, h : Heuristica):
    abiertos = []
    cerrados = set()
    g = {}
    padres = {}
    contador= count()
    inicio=(origen,None)
    g[inicio]=0

    heapq.heappush(abiertos, (h.funcionH(origen, destino), next (contador),0,inicio))
    while abiertos:
        f_actual, _, coste_actual, actual = heapq.heappop(abiertos)
        if coste_actual > g[actual]:
            continue
        if actual in cerrados:
            continue
        
        if actual[0] == destino:
            ruta = reconstruir_camino(padres, actual)
            return ruta, g[actual]
        cerrados.add(actual)
        for conexion in red.conexiones[actual[0]]:
            extremo = conexion.est2
            linea = conexion.linea
            tiempo = conexion.tiempo
            vecino = (extremo, linea)
            peso=g[actual] + tiempo
            if actual[1] is not None and linea != actual[1]:
                clave= (actual[0], actual[1], linea)
                peso= peso+ red.trasbordos[clave]

            if peso < g.get(vecino, float("inf")):
                g[vecino] = peso
                padres[vecino] = actual
                f = peso + h.funcionH(extremo, destino)
                heapq.heappush(abiertos, (f,next(contador), peso, vecino))
                cerrados.discard(vecino)
    return None, float("inf")

def reconstruir_camino(padres,actual):
        ruta = []
        while actual is not None:
            ruta.append(actual[0])
            actual= padres.get(actual)

        ruta.reverse()
        return ruta
