
# MANUAL DE USO
## Proyecto de Seguridad Informática - Grupo 4
### Práctica 4: Inyección SQL, mitigación y seguridad de bases de datos

**Institución:** Universidad Estatal de Milagro (UNEMI)  
**Asignatura:** Seguridad Informática  
**Docente:** Alex Avila  
**Grupo:** 4  

---

## 1. Introducción

Este manual describe los procedimientos necesarios para instalar, configurar y ejecutar los módulos desarrollados para demostrar una vulnerabilidad de inyección SQL, aplicar su mitigación y realizar comprobaciones básicas de seguridad en un entorno local.

Las pruebas están destinadas exclusivamente al entorno académico y controlado del proyecto.

## 2. Requisitos del sistema

- Sistema operativo Windows.
- Python 3 instalado.
- Visual Studio Code (recomendado).
- Conexión a Internet para instalar las dependencias.
- GitHub para consultar el código fuente.

## 3. Estructura del proyecto

El proyecto contiene los siguientes archivos:

```text
grupo4_seguridad_informatica/
│
├── codigo/
│   ├── app_vulnerable.py
│   ├── app_segura.py
│   ├── ataque_sql_i.py
│   ├── escaneo_red.py
│   └── seguridad_bd.py
│
├── evidencia/
│
├── informe/
│
├── resultados/
│
└── .venv/
```

Las bases de datos SQLite se generan o utilizan durante la ejecución local y no deben publicarse si contienen información sensible.

## 4. Instalación y configuración

### 4.1 Descargar el proyecto

Clonar el repositorio desde GitHub:

```powershell
git clone https://github.com/Ariana-Campodonico/grupo4_seguridad_informatica.git
```

Ingresar a la carpeta:

```powershell
cd grupo4_seguridad_informatica
```

### 4.2 Crear el entorno virtual

```powershell
python -m venv .venv
```

### 4.3 Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4.4 Instalar las dependencias

```powershell
python -m pip install flask werkzeug
```

Los módulos de ataque y escaneo utilizan bibliotecas estándar de Python, por lo que no requieren paquetes adicionales.

## 5. Ejecución de la aplicación vulnerable

La aplicación vulnerable permite demostrar el riesgo de construir consultas SQL mediante concatenación de cadenas.

Desde la carpeta principal del proyecto, ejecutar:

```powershell
python .\codigo\app_vulnerable.py
```

Abrir el navegador e ingresar a:

```text
http://127.0.0.1:5000
```

Credenciales de prueba:

- Usuario: admin
- Contraseña: 1234

También se puede comprobar el rechazo de una contraseña incorrecta.

## 6. Prueba de inyección SQL

Con la aplicación vulnerable en funcionamiento, abrir una segunda terminal, activar el entorno virtual y ejecutar:

```powershell
python .\codigo\ataque_sql_i.py
```

El script envía una entrada de prueba diseñada para comprobar si es posible alterar la condición de autenticación.

**Resultado esperado en la versión vulnerable:** el intento consigue acceder, evidenciando el riesgo de inyección SQL.

## 7. Ejecución de la aplicación segura

Primero, detener la aplicación vulnerable utilizando:

```text
Ctrl + C
```

Luego ejecutar:

```powershell
python .\codigo\app_segura.py
```

Abrir nuevamente:

```text
http://127.0.0.1:5000
```

Credenciales de prueba:

- Usuario: admin
- Contraseña: 1234

La aplicación segura utiliza consultas parametrizadas y contraseñas almacenadas mediante hash.

## 8. Comprobación de la mitigación

Con la aplicación segura en funcionamiento, ejecutar desde una segunda terminal:

```powershell
python .\codigo\ataque_sql_i.py
```

**Resultado esperado:** el intento de inyección SQL es rechazado y no permite acceder a la aplicación.

Esto permite comparar el comportamiento de las dos versiones.

## 9. Escaneo básico de puertos

Ejecutar:

```powershell
python .\codigo\escaneo_red.py
```

El módulo examina una lista limitada de puertos TCP en la dirección local:

```text
127.0.0.1
```

Los resultados indican qué puertos aceptan conexiones durante la ejecución. Un puerto abierto no significa necesariamente que exista una vulnerabilidad.

## 10. Revisión de seguridad de la base de datos

Ejecutar:

```powershell
python .\codigo\seguridad_bd.py
```

El módulo realiza comprobaciones básicas de SQLite y presenta recomendaciones de seguridad, como:

- Utilizar consultas parametrizadas.
- Evitar almacenar contraseñas en texto plano.
- Limitar los permisos de acceso a los archivos de base de datos.
- Crear copias de seguridad periódicas.
- Evitar exponer archivos de base de datos en directorios web.
- Mantener mensajes de error genéricos.

## 11. Resultados de las pruebas

Las pruebas realizadas permiten observar la diferencia entre ambas implementaciones:

| Prueba | Resultado |
|---|---|
| Inicio de sesión válido | Acceso permitido |
| Contraseña incorrecta | Acceso rechazado |
| Inyección SQL en versión vulnerable | Intento exitoso |
| Inyección SQL en versión segura | Intento rechazado |
| Escaneo de puertos | Identificación de puertos abiertos |
| Revisión de SQLite | Comprobaciones y recomendaciones |

Los resultados corresponden a las ejecuciones documentadas por el equipo.

## 12. Solución de problemas

**Problema: Python no se reconoce como comando.**

Verificar que Python esté instalado y agregado a las variables de entorno del sistema.

**Problema: No se puede activar el entorno virtual.**

Abrir PowerShell y comprobar que se está ejecutando desde la carpeta principal del proyecto.

**Problema: No se puede instalar Flask.**

Ejecutar:

```powershell
python -m pip install flask werkzeug
```

**Problema: El puerto 5000 está ocupado.**

Detener la aplicación que esté utilizando ese puerto antes de iniciar otra versión.

**Problema: La prueba SQLi no se conecta.**

Comprobar que la aplicación correspondiente esté ejecutándose en:

```text
http://127.0.0.1:5000
```

## 13. Recomendaciones de seguridad

- Ejecutar las pruebas únicamente en sistemas propios o autorizados.
- No utilizar la versión vulnerable en entornos de producción.
- Aplicar consultas parametrizadas en las aplicaciones reales.
- Proteger las credenciales y los archivos de base de datos.
- Mantener actualizadas las dependencias.
- No publicar bases de datos, contraseñas reales ni archivos del entorno virtual.

## 14. Uso académico

Este proyecto fue desarrollado con fines educativos para comprender el funcionamiento de la inyección SQL, sus riesgos y las medidas básicas de mitigación.

**Grupo 4 - Seguridad Informática**  
**Universidad Estatal de Milagro (UNEMI)**
