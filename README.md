
# Tarea Corta 3 - Base de Datos 2

## Profesor: Kenneth Obando Rodríguez

## Integrantes: 
- Luis Gerardo Urbina Salazar
- Andres Mora Urbina

### Fecha de Entrega: 1 de octubre, 2024  

---

## Objetivo:
El objetivo de esta tarea es implementar un clúster de MongoDB con sharding, con tres shards y tres réplicas por shard, simulando una red social de viajes. El sistema debe manejar usuarios, publicaciones, comentarios, likes y seguimientos de manera eficiente a través de esta configuración distribuida. Se debe generar datos sintéticos para simular una base de usuarios a gran escala.

---

## Tabla de Contenidos:
1. [Estructura de la Base de Datos](#estructura-de-la-base-de-datos)
2. [Implementación de Sharding](#implementación-de-sharding)
3. [Generación de Datos](#generación-de-datos)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Scripts y Archivos de Configuración](#scripts-y-archivos-de-configuración)
6. [Problemas Conocidos y Solución de Errores](#problemas-conocidos-y-solución-de-errores)

---

## Estructura de la Base de Datos:

### Usuarios:
- **username**: nombre de usuario único.
- **email**: correo electrónico único.
- **password**: contraseña encriptada.
- **bio**: biografía del usuario.

### Publicaciones:
- **post_text**: texto de la publicación.
- **photo_urls**: lista de URLs de fotos relacionadas.
- **date**: fecha de la publicación.

### Comentarios:
- **comment_text**: texto del comentario.
- **date**: fecha del comentario.

### Likes:
- **user_id**: ID del usuario que dio like.
- **post_id**: ID del post que recibió el like.

### Seguimientos (Follows):
- **follower_id**: ID del usuario que sigue a otro.
- **followed_id**: ID del usuario que es seguido.

---

## Implementación de Sharding:

Se implementó sharding en la base de datos con tres shards, y cada uno tiene tres réplicas. La configuración de cada shard está distribuida para manejar eficientemente grandes cantidades de datos y tráfico.

### Configuración de los Shards:

Cada shard se configuró con las siguientes instancias:

- **Shard 1**:
  - **mongors1n1**: Puerto 27018.
  - **mongors1n2**: Puerto 27019.
  - **mongors1n3**: Puerto 27020.

- **Shard 2**:
  - **mongors2n1**: Puerto 27021.
  - **mongors2n2**: Puerto 27022.
  - **mongors2n3**: Puerto 27023.

- **Shard 3**:
  - **mongors3n1**: Puerto 27024.
  - **mongors3n2**: Puerto 27025.
  - **mongors3n3**: Puerto 27026.

### Config Servers:
Tres servidores de configuración se implementaron para gestionar el clúster de sharding:
- **mongocfg1**: Puerto 27027.
- **mongocfg2**: Puerto 27028.
- **mongocfg3**: Puerto 27029.

### Router (mongos):
El enrutador **mongos** se encargó de distribuir las solicitudes entre los diferentes shards:
- **mongos**: Puerto 27017.

---

## Generación de Datos:

Para simular la base de datos de una red social de viajes, se generaron datos sintéticos utilizando Python y la librería `Faker`. Se crearon 5000 usuarios, 10,000 publicaciones, 50,000 comentarios y 100,000 likes.

El script `data_generator.py` genera y guarda los datos en archivos JSON, para el ejemplo demostrativo solo se usa la coleccion usuarios:

```python
from faker import Faker
import json

fake = Faker()
usuarios = []

for _ in range(5000):
    usuario = {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
        "bio": fake.text(max_nb_chars=150)
    }
    usuarios.append(usuario)

with open('usuarios.json', 'w') as f:
    json.dump(usuarios, f)

print("Archivos generados exitosamente.")
```

El script `data_inserter.py` inserta los datos en el clúster de MongoDB:

```python
from pymongo import MongoClient
import json

client = MongoClient("mongodb://172.25.0.14:27017")
db = client['myTravelDB']

with open('usuarios.json') as f:
    usuarios = json.load(f)

db.usuarios.insert_many(usuarios)
print("Usuarios insertados en la base de datos.")
```

---

## Instalación y Configuración:

### Pre-requisitos:
- Docker.
- Docker Compose.
- Python 3.x.

### Pasos de Instalación:

1. **Clonar el repositorio**:

```bash
git clone <repository-url>
cd <repository-folder>
```

2. **Levantar los contenedores de Docker**:

```bash
docker-compose up -d
```

3. **Verificar el estado de los contenedores**:

```bash
docker ps
```

4. **Ejecutar el script de generación de datos**:

```bash
docker cp data_generator.py mongos:/data_generator.py
docker exec -it mongos bash
python3 /data_generator.py
```

5. **Insertar los datos en la base de datos**:

```bash
docker cp data_inserter.py mongos:/data_inserter.py
docker cp usuarios.json mongos:/usuarios.json
docker exec -it mongos bash
python3 /data_inserter.py
```

---

## Problemas Conocidos y Solución de Errores:

### Error de Timeout:
Si experimentas errores de **ServerSelectionTimeoutError**, es necesario aumentar el tiempo de espera en la configuración de `pymongo`. Añadir las siguientes variables de entorno en el archivo `docker-compose.yml` para asegurar que el cliente pueda conectarse a los servidores de MongoDB sin problemas de timeout.

```yaml
environment:
  - socketTimeoutMS=60000
  - connectTimeoutMS=60000
```

### Uso de RAM y Solución:
Limitamos el uso de memoria de cada contenedor para evitar la sobrecarga de la máquina host. Cada contenedor tiene un límite de 512 MB de RAM para shards y 256 MB para los servidores de configuración.

### Versión de MongoDB:
Se implementó MongoDB versión 6.0.17 para aprovechar las últimas características de estabilidad y rendimiento.

### Ejecución de Scripts dentro del Contenedor:
Los scripts `.sh` fueron utilizados para inicializar los shards y servidores de configuración, mientras que los scripts de inserción de datos se copiaron y ejecutaron dentro del contenedor de `mongos` para asegurar la correcta conectividad con los shards.

### Uso del Dockerfile:
El `Dockerfile` personalizado fue esencial para garantizar que todos los contenedores utilizaran la misma versión de MongoDB. Antes, no se estaba usando un `Dockerfile`, lo que generaba inconsistencias en las versiones.

