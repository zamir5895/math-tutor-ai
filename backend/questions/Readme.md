Cómo correr el proyecto (Linux y Windows)
1. Preparar entorno virtual (recomendado)

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Windows (PowerShell):

python -m venv venv
.\venv\Scripts\Activate.ps1

Windows (CMD):

python -m venv venv
.\venv\Scripts\activate.bat

2. Instalar dependencias

pip install -r requirements.txt

3. Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto con tus datos:

DATASOURCE_USERNAME=miusuario
DATASOURCE_PASSWORD=tu_contraseña
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=mibasedatos

4. Levantar servidor

uvicorn main:app --reload

Esto levantará la API en:
http://127.0.0.1:8000