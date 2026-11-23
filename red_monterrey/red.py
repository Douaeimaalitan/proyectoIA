from .conexion import Conexion
from .estacion import Estacion

class Red:
    def __init__(self):
        self.estaciones = set()
        self.conexiones = {}

    def agregarEstacion(self, estacion):
        self.estaciones.add(estacion)
        if estacion not in self.conexiones:
            self.conexiones[estacion] = set()

    def agregarConexion(self, est1 : Estacion, est2 : Estacion, linea : str, tiempo : float):
        if not isinstance(tiempo, (int,float)) or tiempo <= 0:
            raise ValueError(f"Tiempo suministrado debe ser positivo, no {tiempo!r}")
        self.agregarEstacion(est1)
        self.agregarEstacion(est2)
        self.conexiones[est1].add(Conexion(est1, est2, linea, tiempo))
        self.conexiones[est2].add(Conexion(est2, est1, linea, tiempo))
    def rutaMasRapida(self, origen: Estacion, destino: Estacion, heuristica=None):
        """A* si se pasa una Heuristica; Dijkstra si no.
        Devuelve (tiempo_total, [Conexion, ...], nodos_expandidos) o None si no hay ruta."""
        if origen not in self.estaciones or destino not in self.estaciones:
            return None

        def h(est):
            if heuristica is None or est == destino:
                return 0
            try:
                return heuristica.funcionH(est, destino)
            except KeyError:
                return 0  # sin dato, 0 es admisible (solo pierde eficiencia)

        contador = itertools.count()  # desempata en el heap
        cola = [(h(origen), next(contador), 0, origen)]  # (f, orden, g, estación)
        mejor = {origen: 0}   # mejor g conocido
        previo = {}           # estación -> conexión con la que se llegó
        expandidos = 0

        while cola:
            _, _, g, actual = heapq.heappop(cola)
            if g > mejor.get(actual, float("inf")):
                continue  # entrada antigua
            if actual == destino:
                tramos = []
                while actual in previo:
                    con = previo[actual]
                    tramos.append(con)
                    actual = con.est1
                return g, tramos[::-1], expandidos
            expandidos += 1
            for con in self.conexiones[actual]:
                nuevo = g + con.tiempo
                if nuevo < mejor.get(con.est2, float("inf")):
                    mejor[con.est2] = nuevo
                    previo[con.est2] = con
                    heapq.heappush(cola, (nuevo + h(con.est2), next(contador), nuevo, con.est2))
        return None

    def __str__(self):
        lineas = []
        for estacion in sorted(self.estaciones, key=lambda e: e.nombre):
            lineas.append(f"{estacion}:")
            for con in sorted(self.conexiones[estacion], key=lambda c: c.est2.nombre):
                lineas.append(f"  -> {con.est2} ({con.linea}, {con.tiempo} min)")
        return "\n".join(lineas)