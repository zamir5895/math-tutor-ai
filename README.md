# math-tutor-ai


## Guia para ejecutar todos las base de datos

### Instalar MongoDB

https://www.mongodb.com/try/download/community

### Instalar MongoDB Shell

https://www.mongodb.com/try/download/shell

### BD Usuarios

No necesitamos hacer mucho, solamente editar las variables de entorno siguientes:

Para el siguiente ejemplo se asume que se tiene creada una base de datos llamada NOMBREDB

Como primer paso esta crear la base de datos. Luego:

SPRING_DATASOURCE_URL poner jdbc:postgresql://localhost:5432/NOMBREDB
SPRING_DATASOURCE_USERNAME tu nombre de usuario
SPRING_DATASOURCE_PASSWORD tu contraseña

### Python DB's

Como primer paso debemos entrar al directorio de la base de datos

Luego ejecutamos

Linux: python3 -m venv venv

Windows: python -m venv venv

Finalmente: venv\Scripts\activate

Ahora debemos ejecutar tambien en la carpeta en la terminal:

pip install -r requirements.txt

### Caso IA

Para la IA debemos hacer lo siguiente:

https://github.com/marketplace/models 

Entramos y seleccionamos GPT 4.1 y darle "Use this model" arriba a la derecha y luego a "Get developer key".

Le damos a generate new token ponemos un nombre cualquiera y luego bajamos hasta encontra Account Permisions 

Buscamos Models y le damos Read-only.

Copiamos el token personal de acceso y luego:

set GITHUB_TOKEN=tutokenpegado

y Listo!

Ahora ejecuta con uvicorn main:app --reload


