import sys
from red_monterrey.estacion import Estacion
from red_monterrey.red import Red
from red_monterrey.heuristica import Heuristica
from red_init import construirred
from a_estrella import a_estrella


class HeuristicaFija(Heuristica):
    """Heurística auxiliar con valores controlados por estación para pruebas deterministas."""

    def __init__(self, valores: dict):
        super().__init__({}, 1.0)
        self.valores = valores

    def funcionH(self, origen: Estacion, destino: Estacion):
        if origen == destino:
            return 0
        return self.valores.get(origen, 0)


def _nombres(ruta):
    return [est.nombre for est in ruta] if ruta is not None else None


def test_1_camino_simple_misma_linea():
    a, b, c = Estacion("A"), Estacion("B"), Estacion("C")
    red = Red()
    red.agregarConexion(a, b, "L1", 3)
    red.agregarConexion(b, c, "L1", 5)

    h = Heuristica({a: (0.0, 0.0), b: (3.0, 0.0), c: (8.0, 0.0)}, vel_max=1.0)
    ruta, coste = a_estrella(a, c, red, h)

    if _nombres(ruta) != ["A", "B", "C"]:
        return False, f"Ruta incorrecta: esperada ['A', 'B', 'C'], obtenida {_nombres(ruta)}"
    if coste != 8:
        return False, f"Coste incorrecto: esperado 8, obtenido {coste}"
    return True, "Encuentra la ruta directa A -> B -> C con coste 8"


def test_2_eleccion_mejor_alternativa():
    inicio, lenta, rapida, fin = (
        Estacion("INICIO"),
        Estacion("LENTA"),
        Estacion("RAPIDA"),
        Estacion("FIN"),
    )
    red = Red()
    red.agregarConexion(inicio, lenta, "L1", 10)
    red.agregarConexion(lenta, fin, "L1", 10)
    red.agregarConexion(inicio, rapida, "L1", 4)
    red.agregarConexion(rapida, fin, "L1", 5)

    h = HeuristicaFija({})
    ruta, coste = a_estrella(inicio, fin, red, h)

    if _nombres(ruta) != ["INICIO", "RAPIDA", "FIN"]:
        return False, f"No eligió el camino más corto: obtuvo {_nombres(ruta)}"
    if coste != 9:
        return False, f"Coste incorrecto: esperado 9, obtenido {coste}"
    return True, "Descarta la rama cara (20) y elige la óptima (9)"


def test_3_origen_igual_destino():
    a = Estacion("A")
    red = Red()
    h = Heuristica({a: (0.0, 0.0)}, vel_max=1.0)
    ruta, coste = a_estrella(a, a, red, h)

    if _nombres(ruta) != ["A"]:
        return False, f"Ruta trivial esperada ['A'], obtenida {_nombres(ruta)}"
    if coste != 0:
        return False, f"Coste esperado 0, obtenido {coste}"
    return True, "Devuelve ['A'] con coste 0 cuando origen y destino coinciden"


def test_4_sin_camino_posible():
    a, b, aislada = Estacion("A"), Estacion("B"), Estacion("AISLADA")
    red = Red()
    red.agregarConexion(a, b, "L1", 4)

    h = HeuristicaFija({})
    ruta, coste = a_estrella(a, aislada, red, h)

    if ruta is not None:
        return False, f"Se esperaba None al no existir ruta, pero devolvió {_nombres(ruta)}"
    if coste != float("inf"):
        return False, f"Se esperaba coste inf, pero devolvió {coste}"
    return True, "Devuelve (None, inf) cuando el destino es inalcanzable"


def test_5_trasbordo_entre_lineas():
    e1, e2, e3 = Estacion("E1"), Estacion("E2"), Estacion("E3")
    red = Red()
    red.agregarConexion(e1, e3, "L1", 20)
    red.agregarConexion(e1, e2, "L1", 4)
    red.agregarConexion(e2, e3, "L2", 5)
    red.agregarTrasbordo(e2, "L1", "L2", 3)

    h = Heuristica({e1: (0.0, 0.0), e2: (4.0, 0.0), e3: (9.0, 0.0)}, vel_max=1.0)
    ruta, coste = a_estrella(e1, e3, red, h)

    if _nombres(ruta) != ["E1", "E2", "E3"]:
        return False, f"Ruta esperada ['E1', 'E2', 'E3'], obtenida {_nombres(ruta)}"
    if coste != 12:
        return False, f"Coste esperado 12 (4 + 3 trasbordo + 5), obtenido {coste}"
    return True, "Suma correctamente el tiempo de trasbordo (4 + 3 + 5 = 12)"


def test_6_evita_trasbordo_innecesario():
    e1, e2, e3 = Estacion("E1"), Estacion("E2"), Estacion("E3")
    red = Red()
    red.agregarConexion(e1, e2, "L1", 4)
    red.agregarConexion(e2, e3, "L1", 6)
    red.agregarConexion(e2, e3, "L2", 4)
    red.agregarTrasbordo(e2, "L1", "L2", 5)

    h = HeuristicaFija({})
    ruta, coste = a_estrella(e1, e3, red, h)

    if _nombres(ruta) != ["E1", "E2", "E3"]:
        return False, f"Ruta esperada ['E1', 'E2', 'E3'], obtenida {_nombres(ruta)}"
    if coste != 10:
        return False, f"Debió seguir por L1 (coste 10) en vez de trasbordar (coste 13), obtuvo {coste}"
    return True, "Evita cambiar de línea si el trasbordo encarece el trayecto (10 vs 13)"


def test_7_redireccion_y_propagacion_descendientes():
    origen, a, x, y, destino = (
        Estacion("ORIGEN"),
        Estacion("A"),
        Estacion("X"),
        Estacion("Y"),
        Estacion("DESTINO"),
    )
    red = Red()
    red.agregarConexion(origen, x, "L1", 10)
    red.agregarConexion(origen, a, "L1", 2)
    red.agregarConexion(a, x, "L1", 2)
    red.agregarConexion(x, y, "L1", 3)
    red.agregarConexion(y, destino, "L1", 2)

    # Fuerza que X e Y entren en `cerrados` antes de descubrir el camino óptimo vía A
    h = HeuristicaFija({origen: 0, x: 0, y: 0, a: 12, destino: 0})
    ruta, coste = a_estrella(origen, destino, red, h)

    if _nombres(ruta) != ["ORIGEN", "A", "X", "Y", "DESTINO"]:
        return False, f"No redirigió correctamente a los descendientes: obtuvo {_nombres(ruta)}"
    if coste != 9:
        return False, f"No propagó el ahorro a los descendientes: esperado 9, obtenido {coste}"
    return True, "Redirige padre de nodo cerrado y propaga mejora a descendientes (coste 9)"


def test_8_ciclos_en_grafo_sin_bucle_infinito():
    a, b, c, d = Estacion("A"), Estacion("B"), Estacion("C"), Estacion("D")
    red = Red()
    red.agregarConexion(a, b, "L1", 2)
    red.agregarConexion(b, c, "L1", 2)
    red.agregarConexion(c, a, "L1", 10)
    red.agregarConexion(c, d, "L1", 3)

    h = HeuristicaFija({})
    ruta, coste = a_estrella(a, d, red, h)

    if _nombres(ruta) != ["A", "B", "C", "D"]:
        return False, f"Ruta esperada ['A', 'B', 'C', 'D'], obtenida {_nombres(ruta)} (coste {coste})"
    if coste != 7:
        return False, f"Coste esperado 7, obtenido {coste}"
    return True, "Gestiona ciclos A-B-C sin bucle infinito y elige la ruta óptima (coste 7)"


def test_9_red_monterrey_real():
    red = construirred()
    estaciones_por_nombre = {est.nombre: est for est in red.estaciones}

    if "TALLERES" not in estaciones_por_nombre or "HOSPITAL METROPOLITANO" not in estaciones_por_nombre:
        return False, "No se encontraron las estaciones esperadas en construirred()"

    origen = estaciones_por_nombre["TALLERES"]
    destino = estaciones_por_nombre["HOSPITAL METROPOLITANO"]
    h = HeuristicaFija({})
    ruta, coste = a_estrella(origen, destino, red, h)
    nombres = _nombres(ruta)

    if not nombres or nombres[0] != "TALLERES" or nombres[-1] != "HOSPITAL METROPOLITANO":
        return False, f"Ruta inválida en red real: {nombres}"
    if "CUAUHTÉMOC" not in nombres or "FÉLIX U. GÓMEZ" not in nombres:
        return False, f"Faltan nodos clave de trasbordo en la ruta real: {nombres}"
    if coste <= 0 or coste == float("inf"):
        return False, f"Coste inválido en red real: {coste}"
    return True, f"Ruta válida en Metro de Monterrey ({len(nombres)} estaciones, coste {coste})"


def ejecutar_bateria_pruebas():
    pruebas = [
        ("Test 1 - Camino simple en una línea", test_1_camino_simple_misma_linea),
        ("Test 2 - Elección de rama más rápida", test_2_eleccion_mejor_alternativa),
        ("Test 3 - Origen igual a destino", test_3_origen_igual_destino),
        ("Test 4 - Destino inalcanzable", test_4_sin_camino_posible),
        ("Test 5 - Trasbordo entre líneas", test_5_trasbordo_entre_lineas),
        ("Test 6 - Evitar trasbordo más caro", test_6_evita_trasbordo_innecesario),
        ("Test 7 - Paso 7: redirección y descendientes", test_7_redireccion_y_propagacion_descendientes),
        ("Test 8 - Grafo con ciclos", test_8_ciclos_en_grafo_sin_bucle_infinito),
        ("Test 9 - Red real de Monterrey (L1 -> L2 -> L3)", test_9_red_monterrey_real),
    ]

    superados = 0
    for nombre, funcion_test in pruebas:
        try:
            ok, motivo = funcion_test()
        except Exception as exc:
            ok, motivo = False, f"Excepción {type(exc).__name__}: {exc}"

        estado = "PASS" if ok else "FAIL"
        if ok:
            superados += 1
        print(f"[{estado}] {nombre}: {motivo}")

    print(f"\nResultado final: {superados}/{len(pruebas)} tests superados.")
    if superados != len(pruebas):
        sys.exit(1)


if __name__ == "__main__":
    ejecutar_bateria_pruebas()
