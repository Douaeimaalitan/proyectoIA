class Estacion:
    def __init__(self, nombre : str):
        self.nombre = nombre

    def __eq__(self, otro):
        return isinstance(otro, Estacion) and self.nombre == otro.nombre

    def __hash__(self):
        return hash(self.nombre)

    def __str__(self):
        return self.nombre