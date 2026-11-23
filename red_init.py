from red_monterrey.estacion import Estacion
from red_monterrey.red import Red

def _cargarLinea(red, linea, nombres,tiempos):
    est1 = Estacion(nombres[0])
    for i in range(len(nombres)-1):
        est2 = Estacion(nombres[i + 1])
        red.agregarConexion(est1,est2,'L1',tiempos[i])
        est1 = est2