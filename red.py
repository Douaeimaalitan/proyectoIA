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

        self.agregarEstacion(est1)
        self.agregarEstacion(est2)
        self.conexiones[est1].add(Conexion(est1, est2, linea, tiempo))
        self.conexiones[est2].add(Conexion(est2, est1, linea, tiempo))