
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
from datetime import datetime

# Prueba limitada al laboratorio local autorizado.
URL = "http://127.0.0.1:5000/"

USUARIO_PRUEBA = "' OR '1'='1' -- "
CLAVE_PRUEBA = "cualquiera"


def probar_inyeccion_sql():
    print("=" * 55)
    print("PRUEBA DE INYECCIÓN SQL")
    print("=" * 55)
    print(f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"Aplicación evaluada: {URL}")
    print("Objetivo: comprobar si el formulario resiste la inyección SQL.")
    print("-" * 55)

    datos = urlencode({
        "username": USUARIO_PRUEBA,
        "password": CLAVE_PRUEBA
    }).encode("utf-8")

    solicitud = Request(
        URL,
        data=datos,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )

    try:
        with urlopen(solicitud, timeout=5) as respuesta:
            contenido = respuesta.read().decode(
                "utf-8", errors="replace"
            )

        if "Usuario o contraseña incorrectos" in contenido:
            print("[RESULTADO] El intento fue rechazado.")
            print("Interpretación: la inyección no permitió el acceso.")
        elif "Inicio de sesión correcto" in contenido or "Bienvenido" in contenido:
            print("[RESULTADO] El intento consiguió acceder.")
            print("Interpretación: posible vulnerabilidad de inyección SQL.")
        else:
            print("[AVISO] Respuesta recibida, pero no reconocida.")
            print("Revisa el mensaje mostrado por la aplicación.")

    except HTTPError as error:
        print(f"[ERROR HTTP] La aplicación respondió con código {error.code}.")
    except URLError:
        print("[ERROR] No se pudo conectar con la aplicación.")
        print("Comprueba que el servidor esté ejecutándose en el puerto 5000.")
    except TimeoutError:
        print("[ERROR] La conexión superó el tiempo de espera.")

    print("-" * 55)
    print("Prueba finalizada.")
    print("Alcance: laboratorio local 127.0.0.1.")


if __name__ == "__main__":
    probar_inyeccion_sql()
