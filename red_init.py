from red_monterrey.estacion import Estacion
from red_monterrey.red import Red

nombres1 = ['TALLERES','SAN BERNABÉ', 'UNIDAD MODELO', 'AZTLÁN', 'PENITENCIARÍA', 'ALFONSO REYES', 'MITRAS', 'SIMÓN BOLÍVAR', 'HOSPITAL', 'EDISON', 'CENTRAL', 'CUAUHTÉMOC', 'DEL GOLFO', 'FELIx U.GÓMEZ', 'PARQUE FUNDIDORA','Y GRIEGA', 'ELOY CAVAZOS', 'LERDO DE TEJEDA', 'EXPOSICIÓN']
tiempos1 = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

nombres2 = ['SENDERO', ]
tiempos2 = []

nombres3 = []
tiempos3 = []
def _cargarLinea(red, linea, nombres,tiempos):
    est1 = Estacion(nombres[0])
    for i in range(len(nombres)-1):
        est2 = Estacion(nombres[i + 1])
        red.agregarConexion(est1,est2,linea,tiempos[i])
        est1 = est2

def construirred():
    red = Red()
    _cargarLinea(red,'L1',nombres1, tiempos1)
    _cargarLinea(red,'L2',nombres2, tiempos2)
    _cargarLinea(red,'L3',nombres3, tiempos3)
    return red