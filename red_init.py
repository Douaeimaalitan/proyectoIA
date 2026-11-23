from red_monterrey.estacion import Estacion
from red_monterrey.red import Red

def _cargarLinea(red, linea, nombres,tiempos):
    est1 = Estacion(nombres[0])
    for i in range(len(nombres)-1):
        est2 = Estacion(nombres[i + 1])
        red.agregarConexion(est1,est2,'L1',tiempos[i])
        est1 = est2

def construirred():
    red = Red()
    _cargarLinea(red,'L1',linea1, nombres1, tiempos1)
    _cargarLinea(red,'L2',linea2, nombres2, tiempos2)
    _cargarLinea(red,'L3',linea3, nombres3, tiempos3)
    return red