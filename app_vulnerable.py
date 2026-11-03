import sqlite3
from pathlib import Path

from flask import Flask, request, render_template_string

app = Flask(__name__)

# Base de datos independiente para evitar conflictos con la versión segura
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "usuarios_vulnerable.db"


def conectar_db():
    return sqlite3.connect(DB_PATH)


def preparar_db():
    with conectar_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        conn.execute(
            "INSERT OR IGNORE INTO usuarios (username, password) VALUES (?, ?)",
            ("admin", "1234")
        )
        conn.execute(
            "INSERT OR IGNORE INTO usuarios (username, password) VALUES (?, ?)",
            ("karol", "1234")
        )


PAGINA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Práctica de Seguridad Informática (Vulnerable)</title>
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
                radial-gradient(ellipse at 12% 12%, rgba(232, 74, 74, .13), transparent 34%),
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
            background: linear-gradient(145deg, #df4a34, #b82424);
            box-shadow: 0 7px 16px rgba(187, 37, 37, .22);
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
            color: #ce3434;
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
            border-color: #df4242;
            background: #fff;
            box-shadow: 0 0 0 3px rgba(223, 66, 66, .14);
        }

        button {
            width: 100%;
            min-height: 49px;
            margin-top: 5px;
            border: 0;
            border-radius: 10px;
            background: linear-gradient(110deg, #df4a34, #bd2828);
            color: #fff;
            cursor: pointer;
            font: inherit;
            font-size: 14px;
            font-weight: 700;
            box-shadow: 0 8px 17px rgba(197, 45, 45, .2);
            transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
        }

        button:hover {
            filter: brightness(1.05);
            box-shadow: 0 10px 21px rgba(197, 45, 45, .27);
            transform: translateY(-1px);
        }

        button:focus-visible {
            outline: 3px solid rgba(223, 66, 66, .35);
            outline-offset: 3px;
        }

        button:active {
            transform: translateY(0);
        }

        .message {
            margin: 18px 0 0;
            padding: 12px 14px;
            border: 1px solid #fbd9d9;
            border-radius: 9px;
            background: #fef1f1;
            color: #9d3131;
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
    </style>
</head>
<body>
    <main class="page">
        <div class="brand">
            <div class="brand-mark" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none">
                    <path d="M12 3 19 6v5c0 4.5-2.9 7.7-7 10-4.1-2.3-7-5.5-7-10V6l7-3Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div class="brand-name">Laboratorio (Modo Vulnerable)</div>
                <div class="brand-caption">Demostración de Inyección SQL</div>
            </div>
        </div>

        <section class="card" aria-labelledby="page-title">
            <p class="eyebrow">Acceso Vulnerable</p>
            <h1 id="page-title">Inicia sesión</h1>
            <p class="intro">Formulario sin consultas parametrizadas para pruebas de inyección.</p>

            <form method="POST">
                <div class="field">
                    <label for="username">Usuario</label>
                    <input id="username" type="text" name="username" placeholder="Escribe tu usuario" required>
                </div>

                <div class="field">
                    <label for="password">Contraseña</label>
                    <input id="password" type="password" name="password" placeholder="Escribe tu contraseña" required>
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

        # Consulta intencionalmente vulnerable a SQL Injection mediante concatenación directa
        consulta = (
            "SELECT username FROM usuarios "
            f"WHERE username = '{username}' "
            f"AND password = '{password}'"
        )

        try:
            with conectar_db() as conn:
                usuario = conn.execute(consulta).fetchone()

            if usuario:
                mensaje = f"Inicio de sesión correcto. Bienvenido, {usuario[0]}."
            else:
                mensaje = "Usuario o contraseña incorrectos."

        except sqlite3.Error as err:
            mensaje = f"Error SQL: {err}"

    return render_template_string(PAGINA, mensaje=mensaje)


if __name__ == "__main__":
    preparar_db()
    print("Base de datos vulnerable preparada en usuarios_vulnerable.db.")
    print("Abre http://127.0.0.1:5000 en tu navegador.")
    app.run(host="127.0.0.1", port=5000, debug=False)