import sqlite3
from pathlib import Path

# Obtiene la ruta del directorio donde reside este script
BASE_DIR = Path(__file__).resolve().parent

# Construye la ruta relativa al archivo de base de datos
DB_PATH = BASE_DIR / "usuarios.db"


def revisar_base_datos():
    print("=" * 55)
    print("REVISIÓN BÁSICA DE SEGURIDAD SQLITE")
    print("=" * 55)

    if not DB_PATH.exists():
        print("[AVISO] La base de datos todavía no existe.")
        print(f"Ruta esperada: {DB_PATH.name}")
        print("Ejecuta primero app_segura.py para inicializarla.")
        return

    try:
        # Conexión segura usando context manager
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Comprueba la integridad estructural del archivo SQLite
            cursor.execute("PRAGMA integrity_check")
            resultado_integridad = cursor.fetchone()
            estado_integridad = resultado_integridad[0] if resultado_integridad else "Desconocido"
            print(f"Integridad de la base de datos: {estado_integridad}")

            # Lista las tablas creadas por el usuario excluyendo internas
            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
            """)
            tablas = cursor.fetchall()

            print("\nTablas encontradas:")
            if tablas:
                for tabla in tablas:
                    print(f"- {tabla[0]}")
            else:
                print("- No se encontraron tablas de usuario.")

            # Comprueba si el motor valida claves foráneas
            cursor.execute("PRAGMA foreign_keys")
            fk_resultado = cursor.fetchone()
            claves_foraneas = fk_resultado[0] if fk_resultado else 0

            estado_fk = "activadas" if claves_foraneas == 1 else "desactivadas"
            print(f"\nClaves foráneas: {estado_fk}")

            print("\nBuenas prácticas recomendadas:")
            print("- Usar consultas parametrizadas.")
            print("- No guardar contraseñas en texto plano.")
            print("- Limitar permisos de acceso al archivo .db.")
            print("- Crear copias de seguridad periódicas.")
            print("- No exponer la base de datos al directorio web.")
            print("- Mantener mensajes de error genéricos.")

    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo revisar la base de datos: {error}")


if __name__ == "__main__":
    revisar_base_datos()