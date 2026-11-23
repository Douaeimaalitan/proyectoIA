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
    def __str__(self):
        return f"{self.est1} -> {self.est2} ({self.linea}, {self.tiempo} min)"
    def __repr__(self):
        return f"Conexion({self.est1!r}, {self.est2!r}, {self.linea!r}, {self.tiempo!r})"
        # el !r es para diferenciar un string de un número (3 vs '3') y se ven mejor los errores.
        # SOLO PARA NOSOTROS; LUEGO BORRAR, los mensajes usar el str