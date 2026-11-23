import sys 
from pathlib import Path
from red_monterrey.estacion import Estacion
from red_monterrey.red import Red
from red_monterrey.heuristica import Heuristica
from a_estrella import a_estrella
from PySide6.QtWidgets import (QApplication, QComboBox, QPushButton, QTextEdit)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import (QFile, QObject)

app = QApplication(sys.argv)
# cargamos interfaz
ruta_mapa = Path(__file__).resolve().parent / "metro.ui"
fich = QFile(str(ruta_mapa))
if not fich.open(QFile.ReadOnly):
    raise RuntimeError("No se pudo abrir fichero")
ventana = QUiLoader().load(fich)
fich.close()
#cargamos estaciones
estaciones = { "boton_Talleres": "Talleres",
    "boton_SanBernabe": "San Bernabé",
    "boton_UnidadModelo": "Unidad Modelo",
    "boton_Aztlan": "Aztlán",
    "boton_Penitenciaria": "Penitenciaría",
    "boton_AlfonsoReyes": "Alfonso Reyes",
    "boton_Mitras": "Mitras",
    "boton_SimonBolivar": "Simón Bolívar",
    "boton_Hospital": "Hospital",
    "boton_Edison": "Edison",
    "boton_Central": "Central",
    "boton_Cuauhtemoc": "Cuauhtémoc",
    "boton_DelGolfo": "Del Golfo",
    "boton_FelixUGomez": "Félix U. Gómez",
    "boton_YGriega": "Y Griega",
    "boton_ParqueFundidora": "Parque Fundidora",
    "boton_EloyCavazos": "Eloy Cavazos",
    "boton_LerdoDeTejeda": "Lerdo de Tejeda",
    "boton_Exposicion": "Exposición",
    "boton_Sendero": "Sendero",
    "boton_SantiagoTapia": "Santiago Tapia",
    "boton_SanNicolas": "San Nicolás",
    "boton_Anahuac": "Anáhuac",
    "boton_Universidad": "Universidad",
    "boton_NinosHeroes": "Niños Héroes",
    "boton_Regina": "Regina",
    "boton_GralAnaya": "General Anaya",
    "boton_Alameda": "Alameda",
    "boton_Fundadores": "Fundadores",
    "boton_PadreMier": "Padre Mier",
    "boton_GralIZaragoza": "General I. Zaragoza",
    "boton_SantaLucia": "Santa Lucía",
    "boton_ColObrera": "Colonia Obrera",
    "boton_Metalurgicos": "Metalúrgicos",
    "boton_ColModerna": "Colonia Moderna",
    "boton_RuizCortines": "Ruiz Cortines",
    "boton_LosAngeles": "Los Ángeles",
    "boton_HospitalMetropolitano": "Hospital Metropolitano"}

#conectamos componentes
boton_calcular = ventana.findChild(QPushButton, "boton_Calcular")
boton_limpiar = ventana.findChild( QPushButton, "boton_Limpiar")
est_origen = ventana.findChild(QComboBox, "est_Origen")
est_destino = ventana.findChild(QComboBox, "est_Destino")
result = ventana.findChild(QTextEdit, "txt_Resultado")

def calcular_ruta():
    if (est_origen.currentIndex() == 0 or est_destino.currentIndex() == 0):
        result.setPlainText("Selecciona origen y destino.")
        return
    origen = est_origen.currentText()
    destino = est_destino.currentText()
    if (origen == destino):
        result.setPlainText("Coincide el destino con el origen")
    else: 
        result.setPlainText(f"Origen: {origen}\n" 
        f"Destino: {destino}\n")

#rellenamos los botones
nombres_est = list(estaciones.values())
est_origen.clear()
est_destino.clear()
est_origen.addItem("Seleccionar origen")
est_origen.addItems(nombres_est)
est_destino.addItem("Seleccionar destino")
est_destino.addItems(nombres_est)

def seleccionar_estacion(est):
    if (est_origen.currentIndex() == 0):
        est_origen.setCurrentText(est)

    elif (est_destino.currentIndex() == 0):
        est_destino.setCurrentText(est)

    else:
        est_origen.setCurrentText(est)
        est_destino.setCurrentIndex(0)

class ReceptorBotones(QObject):
    def pulsar_boton(self):
        boton = self.sender() #sender permite saber que componente ha provocado una accion
        nombre_boton = boton.objectName()
        nombre_estacion = estaciones[nombre_boton]
        seleccionar_estacion(nombre_estacion)

recep = ReceptorBotones()
for nombre_boton in estaciones:
    boton = ventana.findChild(QPushButton, nombre_boton)
    if boton is not None:
        boton.clicked.connect(recep.pulsar_boton)

def limpiar():
    est_origen.setCurrentIndex(0)
    est_destino.setCurrentIndex(0)
    result.clear()
#
boton_calcular.clicked.connect(calcular_ruta)
boton_limpiar.clicked.connect(limpiar)
# mostramos interfaz
# Prueba temporal del algoritmo A*
a = Estacion("A")
b = Estacion("B")
c = Estacion("C")

red = Red()

red.agregarConexion(a, b, "L1", 4)
red.agregarConexion(b, c, "L1", 4)
red.agregarConexion(a, c, "L1", 15)

h = Heuristica()

h.agregarH(a, c, 0)
h.agregarH(b, c, 0)

ruta, tiempo = a_estrella(a, c, red, h)

print("Ruta:", " -> ".join(str(e) for e in ruta))
print("Tiempo:", tiempo, "minutos")
ventana.show()
sys.exit(app.exec())
