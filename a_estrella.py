import heapq
from itertools import count
from red_monterrey.estacion import Estacion
from red_monterrey.conexion import Conexion
from red_monterrey.red import Red
from red_monterrey.heuristica import Heuristica

def a_estrella(origen : Estacion, destino : Estacion, red : Red, h : Heuristica):
    abiertos = []
    cerrados = set()
    g = {}
    padres = {}
    hijos = {} #sino no se a que hijos he de comprobar su coste
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
            ruta = _reconstruir_camino(padres, actual)
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
                #Comprobar si el vecino estaba en cerrados para actualizar sus descendientes 
                # (luego lo quito de cerrados y por eso está tan arriba)
                estaba_en_cerrados = vecino in cerrados
                padre_anterior = padres.get(vecino)
                #eliminar a vecino de los hijos del padre anterior (si es que estaba siquiera)
                if padre_anterior is not None and padre_anterior != actual:
                    hijos.get(padre_anterior, set()).discard(vecino)
                g[vecino] = peso
                padres[vecino] = actual
                # Se añade como hijo a vecino siempre y si no tenia hijos actual, se crea un set vacío antes
                hijos.setdefault(actual, set()).add(vecino)
                f = peso + h.funcionH(extremo, destino)
                heapq.heappush(abiertos, (f,next(contador), peso, vecino))
                cerrados.discard(vecino)
                #Este es el 7.2 per se, que lo hago con dos funciones extra que sino es muy largo
                if estaba_en_cerrados:
                    _actualizar_descendientes(vecino, g, padres, hijos, red, abiertos, cerrados,
                                              contador,destino, h)
    return None, float("inf")

def _reconstruir_camino(padres,actual):
        ruta = []
        while actual is not None:
            ruta.append(actual[0])
            actual= padres.get(actual)

        ruta.reverse()
        return ruta

#tiempo del tramo entre dos estaciones, incluyendo el tiempo de trasbordo si es necesario
def _coste_directo(padre_estado, hijo_estado, red):
    est_p, linea_p = padre_estado
    est_h, linea_h = hijo_estado
    for conex in red.conexiones[est_p]:
        if conex.est2 == est_h and conex.linea == linea_h:
            coste = conex.tiempo
            if linea_p is not None and linea_p != linea_h:
                clave = (est_p, linea_p, linea_h)
                coste += red.trasbordos[clave]
            return coste
    return float("inf")  # Si no hay conexión directa

#recorre uno a uno los descendientes de nodo_raiz y actualiza su coste si es menor que el anterior,
#y si es así, añade a los descendientes a la pila para seguir comprobando sus descendentes, así recursivamente.
def _actualizar_descendientes(nodo_raiz, g, padres, hijos, red, abiertos, cerrados,
                              contador,destino, h):
    pila = list(hijos.get(nodo_raiz, ())) #hijos del nodo que ha cambiado el coste
    while pila:
        desc = pila.pop()
        if padres.get(desc) != nodo_raiz: #compruebo que siga siendo el padre por si se ha cambiado
            continue
        coste_tramo = _coste_directo(nodo_raiz, desc, red)
        nuevo_g = g[nodo_raiz] + coste_tramo #actualiza g
        if nuevo_g < g.get(desc, float("inf")):
            g[desc] = nuevo_g
            f_desc = nuevo_g + h.funcionH(desc[0], destino)
            heapq.heappush(abiertos, (f_desc, next(contador), nuevo_g, desc))
            cerrados.discard(desc)
            pila.extend(hijos.get(desc, ())) #Seguimos explorando descendientes