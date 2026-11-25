from red_monterrey.estacion import Estacion
from math import sqrt
def distancia(c1,c2):
    latit1, long1=c1
    latit2, long2=c2
    return sqrt((latit1-latit2)**2 + (long1-long2)**2)

def calcular_vel_max(red,coords):
    vel_max=0
    for conexiones in red.conexiones.values():
        for c in conexiones:
            vel= distancia(coords[c.est1],coords[c.est2])/c.tiempo
            if vel> vel_max:
                vel_max=vel
    return vel_max

class Heuristica:

    def __init__(self,coords,vel_max):
        self.coords=coords 
        self.vel_max=vel_max


    def funcionH(self, origen : Estacion, destino : Estacion):
        if origen== destino:
            return 0
        return distancia(self.coords[origen],self.coords[destino])/ self.vel_max