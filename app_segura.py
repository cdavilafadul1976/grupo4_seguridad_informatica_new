from pathlib import Path
import sqlite3

from flask import Flask, request, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Definición de ruta dinámica y segura hacia usuarios.db
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "usuarios.db"


def conectar_db():
    return sqlite3.connect(DB_PATH)


def preparar_db():
    with conectar_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        usuarios_iniciales = [
            ("admin", "1234"),
            ("karol", "1234")
        ]

        for username, password in usuarios_iniciales:
            existe = conn.execute(
                "SELECT 1 FROM usuarios WHERE username = ?",
                (username,)
            ).fetchone()

            if not existe:
                password_hash = generate_password_hash(password)
                conn.execute(
                    "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )


PAGINA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Práctica de Seguridad Informática</title>
    <style>
        :root {
            color-scheme: light;
            font-family: "Segoe UI", Arial, sans-serif;
            color: #172b4d;
            background: #f3f6fb;
            font-synthesis: none;
            text-rendering: optimizeLegibility;
        }

        * {
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            margin: 0;
            display: grid;
            place-items: center;
            padding: 32px 18px;
            background:
                radial-gradient(ellipse at 12% 12%, rgba(74, 130, 232, .13), transparent 34%),
                radial-gradient(ellipse at 90% 88%, rgba(24, 166, 153, .10), transparent 30%),
                #f3f6fb;
        }

        .page {
            width: min(100%, 440px);
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 0 0 22px 4px;
            color: #24436e;
        }

        .brand-mark {
            width: 42px;
            height: 42px;
            display: grid;
            place-items: center;
            border-radius: 13px;
            color: #fff;
            background: linear-gradient(145deg, #3478df, #2456b8);
            box-shadow: 0 7px 16px rgba(37, 91, 187, .22);
        }

        .brand-mark svg {
            width: 23px;
            height: 23px;
        }

        .brand-name {
            font-size: 14px;
            font-weight: 700;
            letter-spacing: .02em;
        }

        .brand-caption {
            margin-top: 3px;
            color: #74839b;
            font-size: 12px;
        }

        .card {
            padding: 38px;
            border: 1px solid #e5eaf2;
            border-radius: 20px;
            background: #fff;
            box-shadow: 0 22px 55px rgba(28, 48, 82, .10);
        }

        .eyebrow {
            margin: 0 0 10px;
            color: #3472ce;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .13em;
            text-transform: uppercase;
        }

        h1 {
            margin: 0;
            color: #172b4d;
            font-size: clamp(25px, 6vw, 30px);
            letter-spacing: -.04em;
            line-height: 1.2;
        }

        .intro {
            margin: 12px 0 28px;
            color: #6b7890;
            font-size: 14px;
            line-height: 1.6;
        }

        .field {
            margin-bottom: 19px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #344665;
            font-size: 13px;
            font-weight: 600;
        }

        input {
            width: 100%;
            min-height: 48px;
            padding: 12px 14px;
            border: 1px solid #dce3ed;
            border-radius: 10px;
            outline: none;
            background: #fbfcfe;
            color: #172b4d;
            font: inherit;
            font-size: 14px;
            transition: border-color .18s ease, box-shadow .18s ease, background .18s ease;
        }

        input::placeholder {
            color: #a0aabc;
        }

        input:focus {
            border-color: #4281df;
            background: #fff;
            box-shadow: 0 0 0 3px rgba(66, 129, 223, .14);
        }

        button {
            width: 100%;
            min-height: 49px;
            margin-top: 5px;
            border: 0;
            border-radius: 10px;
            background: linear-gradient(110deg, #3478df, #285bbd);
            color: #fff;
            cursor: pointer;
            font: inherit;
            font-size: 14px;
            font-weight: 700;
            box-shadow: 0 8px 17px rgba(45, 101, 197, .2);
            transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
        }

        button:hover {
            filter: brightness(1.05);
            box-shadow: 0 10px 21px rgba(45, 101, 197, .27);
            transform: translateY(-1px);
        }

        button:focus-visible {
            outline: 3px solid rgba(66, 129, 223, .35);
            outline-offset: 3px;
        }

        button:active {
            transform: translateY(0);
        }

        .message {
            margin: 18px 0 0;
            padding: 12px 14px;
            border: 1px solid #d9e7fb;
            border-radius: 9px;
            background: #f1f6fe;
            color: #315d9d;
            font-size: 13px;
            line-height: 1.5;
        }

        .footer {
            margin: 20px 8px 0;
            color: #78869c;
            font-size: 12px;
            line-height: 1.6;
            text-align: center;
        }

        @media (max-width: 480px) {
            .card {
                padding: 30px 24px;
                border-radius: 16px;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                scroll-behavior: auto !important;
                transition-duration: .01ms !important;
            }
        }
    </style>
</head>
<body>
    <main class="page">
        <div class="brand">
            <div class="brand-mark" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                    <path d="M12 3 19 6v5c0 4.5-2.9 7.7-7 10-4.1-2.3-7-5.5-7-10V6l7-3Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
                    <path d="m9 12 2 2 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div class="brand-name">Laboratorio de Seguridad</div>
                <div class="brand-caption">Práctica de seguridad informática</div>
            </div>
        </div>

        <section class="card" aria-labelledby="page-title">
            <p class="eyebrow">Acceso al laboratorio</p>
            <h1 id="page-title">Inicia sesión</h1>
            <p class="intro">Ingresa tus credenciales para continuar con el entorno de práctica.</p>

            <form method="POST">
                <div class="field">
                    <label for="username">Usuario</label>
                    <input id="username" type="text" name="username" placeholder="Escribe tu usuario" autocomplete="username" required>
                </div>

                <div class="field">
                    <label for="password">Contraseña</label>
                    <input id="password" type="password" name="password" placeholder="Escribe tu contraseña" autocomplete="current-password" required>
                </div>

                <button type="submit">Iniciar sesión</button>
            </form>

            {% if mensaje %}
                <p class="message" role="status" aria-live="polite">{{ mensaje }}</p>
            {% endif %}
        </section>

        <p class="footer">Entorno de práctica local · Flask + SQLite</p>
    </main>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        consulta = """
            SELECT username, password_hash
            FROM usuarios
            WHERE username = ?
        """

        try:
            with conectar_db() as conn:
                usuario = conn.execute(
                    consulta, (username,)
                ).fetchone()

            if usuario and check_password_hash(usuario[1], password):
                mensaje = f"Inicio de sesión correcto. Bienvenido, {usuario[0]}."
            else:
                mensaje = "Usuario o contraseña incorrectos."

        except sqlite3.Error:
            mensaje = "Se produjo un error al consultar la base de datos."

    return render_template_string(PAGINA, mensaje=mensaje)


if __name__ == "__main__":
    preparar_db()
    print("Base de datos preparada.")
    print("Versión corregida en http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)