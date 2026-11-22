from .estacion import Estacion

class Conexion:
    def __init__(self, est1 : Estacion, est2 : Estacion, linea : str, tiempo : float):
        self.est1 = est1
        self.est2 = est2
        self.linea = linea
        self.tiempo = tiempo

    def __eq__(self, otro):
        return isinstance(otro, Conexion) and self.est1 == otro.est1 and self.est2 == otro.est2 and self.linea == otro.linea and self.tiempo == otro.tiempo

    def __hash__(self):
        return hash((self.est1, self.est2, self.linea, self.tiempo))