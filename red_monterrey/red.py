from .conexion import Conexion
from .estacion import Estacion

class Red:
    def __init__(self):
        self.estaciones = set()
        self.conexiones = {}
        self.trasbordos= {}

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
    def agregarTrasbordo(self, estacion, linea1, linea2, tiempo):
        self.trasbordos[(estacion, linea1, linea2)] = tiempo
        self.trasbordos[(estacion, linea2, linea1)] = tiempo
    def __str__(self):
        lineas = []
        for estacion in sorted(self.estaciones, key=lambda e: e.nombre):
            lineas.append(f"{estacion}:")
            for con in sorted(self.conexiones[estacion], key=lambda c: c.est2.nombre):
                lineas.append(f"  -> {con.est2} ({con.linea}, {con.tiempo} min)")
        return "\n".join(lineas)