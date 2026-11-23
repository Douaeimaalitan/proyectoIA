from red_init import construirred
from red_monterrey.estacion import Estacion
from a_estrella import a_estrella

class HeuristicaCero:
    def funcionH(self, origen, destino):
        return 0

red = construirred()
h = HeuristicaCero()

# 1. Estructura de la red
print("Estaciones:", len(red.estaciones), "(esperado 38)")
trasb = sorted(str(e) for e, cons in red.conexiones.items()
               if len({c.linea for c in cons}) > 1)
print("Transbordos:", trasb)
print()

# 2. Rutas con resultado conocido (tiempos de 3 min y transbordo de 4)
casos = [
    ("TALLERES", "EXPOSICIÓN", 54),                  # solo L1, 18 tramos
    ("SENDERO", "TALLERES", 61),                      # L2 -> Cuauhtémoc -> L1
    ("HOSPITAL METROPOLITANO", "SENDERO", 53),        # L3 -> Félix -> L1 -> Cuauhtémoc -> L2
    ("MITRAS", "MITRAS", 0),                          # origen = destino
]

for origen, destino, esperado in casos:
    ruta, tiempo = a_estrella(Estacion(origen), Estacion(destino), red, h)
    estado = "OK" if tiempo == esperado else "FALLO"
    print(f"[{estado}] {origen} -> {destino}: {tiempo} min (esperado {esperado})")
    print("   ", " -> ".join(str(e) for e in ruta))