from red_monterrey.estacion import Estacion
from red_monterrey.conexion import Conexion
from red_monterrey.red import Red

def main():
    atocha = Estacion("Atocha")
    sol = Estacion("Sol")
    conexion = Conexion(atocha, sol, "L2", "3")
    red = Red()
    red.agregarConexion(atocha, sol, "L2", "3")
    print(conexion)
    print(atocha)
    return 0

if __name__ == "__main__":
    main() este es el main, no es el definitivo