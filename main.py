from red_monterrey.estacion import Estacion
from red_monterrey.conexion import Conexion
from red_monterrey.red import Red

def main():
    atocha = Estacion("Atocha")
    sol = Estacion("Sol")
    #con el metodo str que he metido en conexión no hace falta meter esta linea ni el print
    red = Red()
    red.agregarConexion(atocha, sol, "L2", "3")
    for con in red.conexiones[atocha]:
        print (con)
    return 0

if __name__ == "__main__":
    main() #este es el main, no es el definitivo