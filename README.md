INSTRUCCIONES DE EJECUCIÓN DEL PROYECTO

Requisitos previos:
- Tener instalado Python 3.

Pasos para ejecutar:
1. Abrir una terminal en esta carpeta.
2. Instalar las dependencias necesarias:
   pip install -r requirements.txt

3. Ejecución de los módulos del proyecto:
   - Para iniciar la aplicación web segura:
     python codigo/app_segura.py
     (Abrir luego en el navegador http://127.0.0.1:5000)

   - Para revisar el estado y seguridad de la base de datos:
     python codigo/seguridad_bd.py

   - Para la aplicación vulnerable (demostración de fallas):
     python codigo/app_vulnerable.py

   - Para la prueba de inyección SQL:
     python codigo/ataque_sql_i.py

   - Para el escaneo de red:
     python codigo/escaneo_red.py