from red_monterrey.estacion import Estacion
from red_monterrey.red import Red

nombres1 = ['TALLERES', 'SAN BERNABÉ', 'UNIDAD MODELO', 'AZTLÁN', 'PENITENCIARÍA',
            'ALFONSO REYES', 'MITRAS', 'SIMÓN BOLÍVAR', 'HOSPITAL', 'EDISON', 'CENTRAL',
            'CUAUHTÉMOC', 'DEL GOLFO', 'FÉLIX U. GÓMEZ', 'PARQUE FUNDIDORA', 'Y GRIEGA',
            'ELOY CAVAZOS', 'LERDO DE TEJEDA', 'EXPOSICIÓN']
tiempos1 = [3] * (len(nombres1) - 1)   # 18

nombres2 = ['SENDERO', 'SANTIAGO TAPIA', 'SAN NICOLÁS', 'ANÁHUAC', 'UNIVERSIDAD',
            'NIÑOS HÉROES', 'REGINA', 'GENERAL ANAYA', 'CUAUHTÉMOC', 'ALAMEDA',
            'FUNDADORES', 'PADRE MIER', 'GENERAL I. ZARAGOZA']
tiempos2 = [3] * (len(nombres2) - 1)   # 12

nombres3 = ['HOSPITAL METROPOLITANO', 'LOS ÁNGELES', 'RUIZ CORTINES', 'COLONIA MODERNA',
            'METALÚRGICOS', 'FÉLIX U. GÓMEZ', 'COLONIA OBRERA', 'SANTA LUCÍA',
            'GENERAL I. ZARAGOZA']
tiempos3 = [3] * (len(nombres3) - 1)   # 8
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