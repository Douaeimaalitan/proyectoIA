from red_monterrey.estacion import Estacion

class Heuristica:

    def __init__(self):
        self.h = {}

    def agregarH(self, origen : Estacion, destino : Estacion, tiempo : float):
        if origen not in self.h:
            self.h[origen] = {}
        if destino not in self.h:
            self.h[destino] = {}
        self.h[origen][destino] = tiempo
        self.h[destino][origen] = tiempo

    def funcionH(self, origen : Estacion, destino : Estacion):
        return self.h[origen][destino]