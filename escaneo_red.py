
import socket
from datetime import datetime

# Escaneo básico únicamente en el equipo local.
HOST = "127.0.0.1"

# Puertos habituales para comprobar servicios locales.
PUERTOS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5000: "Flask / desarrollo web",
    5432: "PostgreSQL",
    8000: "Servidor web alternativo",
    8080: "HTTP alternativo",
}


def comprobar_puerto(host, puerto):
    """Comprueba si un puerto TCP acepta conexiones."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexion:
            conexion.settimeout(0.5)
            resultado = conexion.connect_ex((host, puerto))
            return resultado == 0
    except OSError:
        return False


def main():
    print("=" * 55)
    print("MÓDULO DE ESCANEO BÁSICO DE RED")
    print("=" * 55)
    print(f"Equipo analizado: {HOST}")
    print(f"Fecha y hora: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("-" * 55)

    abiertos = 0

    for puerto, servicio in PUERTOS.items():
        if comprobar_puerto(HOST, puerto):
            print(f"[ABIERTO] Puerto {puerto:<5} Servicio: {servicio}")
            abiertos += 1
        else:
            print(f"[CERRADO] Puerto {puerto:<5} Servicio esperado: {servicio}")

    print("-" * 55)
    print(f"Puertos abiertos encontrados: {abiertos}")
    print("Escaneo finalizado.")
    print("Alcance: equipo local autorizado (127.0.0.1).")


if __name__ == "__main__":
    main()
