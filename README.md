
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
3. [Configuración de Sharding ](#4-copiar-scripts-en-los-contenedores-ejecutarlos-y-verificar-conexiones)
4. [Generación de Datos](#generación-de-datos)
5. [Instalación y Configuración](#instalación-y-configuración)
6. [Scripts y Archivos de Configuración](#scripts-y-archivos-de-configuración)
7. [Particionamiento Utilizada](#estrategia-de-particionamiento-utilizada)
8. [Consistencia entre Réplicas](#manejo-de-la-consistencia-entre-réplicas)
9. [Problemas Conocidos y Solución de Errores](#problemas-conocidos-y-solución-de-errores)

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

## Copiar Scripts en los Contenedores, Ejecutarlos y Verificar Conexiones

Este apartado explica cómo copiar los scripts en los contenedores, ejecutarlos y verificar que todo esté funcionando correctamente.

### 4.1 Copiar Scripts en los Contenedores

Para copiar los scripts en los contenedores correspondientes, utilizamos el comando `docker cp`. Los scripts necesarios incluyen:

- `init_config_servers.sh`: Inicializa el conjunto de réplicas para los servidores de configuración.
- `init_shard1.sh`, `init_shard2.sh`, `init_shard3.sh`: Inicializan los conjuntos de réplicas para cada uno de los shards.
- `add_shards.sh`: Añade los shards al router (mongos).
- `enable_sharding.sh`: Habilita el sharding en la base de datos.

#### Ejemplo de comandos para copiar scripts:
```bash
# Copiar script de inicialización de los servidores de configuración
docker cp init_config_servers.sh mongocfg1:/init_config_servers.sh

# Copiar script de inicialización de Shard 1
docker cp init_shard1.sh mongors1n1:/init_shard1.sh

# Copiar script de inicialización de Shard 2
docker cp init_shard2.sh mongors2n1:/init_shard2.sh

# Copiar script de inicialización de Shard 3
docker cp init_shard3.sh mongors3n1:/init_shard3.sh

# Copiar script para añadir los shards
docker cp add_shards.sh mongos:/add_shards.sh

# Copiar script para habilitar el sharding
docker cp enable_sharding.sh mongos:/enable_sharding.sh
```
### 4.2 Ejecutar los Scripts
  
Una vez copiados los scripts, es necesario ejecutarlos dentro de los contenedores para configurar los shards y los servidores de configuración.

Comandos para ejecutar los scripts:

```bash
# Ejecutar script de inicialización de los servidores de configuración
docker exec -it mongocfg1 bash -c "bash /init_config_servers.sh"

# Ejecutar script de inicialización de Shard 1
docker exec -it mongors1n1 bash -c "bash /init_shard1.sh"

# Ejecutar script de inicialización de Shard 2
docker exec -it mongors2n1 bash -c "bash /init_shard2.sh"

# Ejecutar script de inicialización de Shard 3
docker exec -it mongors3n1 bash -c "bash /init_shard3.sh"

# Ejecutar script para añadir los shards al router
docker exec -it mongos bash -c "bash /add_shards.sh"

# Ejecutar el script para habilitar el sharding
docker exec -it mongos bash -c "bash /enable_sharding.sh"
```


### 4.3 Verificar las Conexiones y Estado de los Shards
Para verificar que los shards y los servidores de configuración se han configurado correctamente, puedes ingresar a los contenedores y consultar el estado de los conjuntos de réplicas.

Comandos para verificar el estado:

```bash
# Ingresar al contenedor de mongos y verificar los shards
docker exec -it mongos mongosh --eval "sh.status()"

# Ingresar al contenedor de Shard 1 y verificar su estado
docker exec -it mongors1n1 mongosh --eval "rs.status()"

# Ingresar al contenedor de Shard 2 y verificar su estado
docker exec -it mongors2n1 mongosh --eval "rs.status()"

# Ingresar al contenedor de Shard 3 y verificar su estado
docker exec -it mongors3n1 mongosh --eval "rs.status()"

# Ingresar al contenedor de los servidores de configuración y verificar su estado
docker exec -it mongocfg1 mongosh --eval "rs.status()"
```

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
git clone https://github.com/LUISGM1501/DB_TC3
cd DB_TC3
```

2. **Levantar los contenedores de Docker**:

```bash
docker-compose up -d
```

3. **Verificar el estado de los contenedores**:

```bash
docker ps
```

4. **Instalar Python y Pymongo**:

```bash
docker exec -it mongos bash
apt-get update && apt-get install -y python3-pip
pip3 install pymongo
```

5. **Habilitar el sharding en la base de datos**:

```bash
sh.enableSharding("myTravelDB")
```

Para cada colección (usuarios, posts, comentarios, likes, follows), necesitamos crear un índice hashed sobre la clave de particionamiento (_id) y luego habilitar el sharding para esa colección. Ejecuta los siguientes comandos:

```bash
Copiar código
db.usuarios.createIndex({ _id: "hashed" });
sh.shardCollection("myTravelDB.usuarios", { _id: "hashed" });

db.posts.createIndex({ _id: "hashed" });
sh.shardCollection("myTravelDB.posts", { _id: "hashed" });

db.comentarios.createIndex({ _id: "hashed" });
sh.shardCollection("myTravelDB.comentarios", { _id: "hashed" });

db.likes.createIndex({ _id: "hashed" });
sh.shardCollection("myTravelDB.likes", { _id: "hashed" });

db.follows.createIndex({ _id: "hashed" });
sh.shardCollection("myTravelDB.follows", { _id: "hashed" });
```

6. **Ejecutar el script de generación de datos**:

```bash
docker cp data_generator.py mongos:/data_generator.py
docker exec -it mongos bash
python3 /data_generator.py
```

7. **Insertar los datos en la base de datos**:

Este paso puede llegar a durar varios minutoss.

```bash
docker cp data_inserter.py mongos:/data_inserter.py
docker cp usuarios.json mongos:/usuarios.json
docker exec -it mongos bash
python3 /data_inserter.py
```

8. **Verificar la inserción de datos**:

Verificar que los datos están correctamente insertados en tu base de datos MongoDB haciendo algunas consultas básicas.

Primero ingresa al contenedor de mongos:
```bash
docker exec -it mongos bash
```
Conectar a MongoDB usando mongosh:
```bash
mongosh --host 172.18.0.14 --port 27017
```
Seleccionar la base de datos:
```bash
use myTravelDB
```

Verificamos los datos:
```bash
db.usuarios.find().pretty()
db.posts.find().pretty()
db.comentarios.find().pretty()
db.likes.find().pretty()
db.follows.find().pretty()
```


9. **Verificar el recuento total de documentos en cada colección**:

```bash
db.usuarios.countDocuments()
db.posts.countDocuments()
db.comentarios.countDocuments()
db.likes.countDocuments()
db.follows.countDocuments()
```

10. **Verificar el estado de la base de datos particionada**:

Entra al contenedor donde corre mongos
```bash
docker exec -it mongos bash
```
Abrir el shell de MongoDB (mongosh):
```bash
mongosh --host 127.0.0.1 --port 27017
```

Seleccionar la base de datos:
```bash
use myTravelDB
```

Verifica la distribución de los datos en los shards utilizando el comando getShardDistribution() para cada colección:

```bash
db.usuarios.getShardDistribution();
db.posts.getShardDistribution();
db.comentarios.getShardDistribution();
db.likes.getShardDistribution();
db.follows.getShardDistribution();
```


---

## Estrategia de Particionamiento Utilizada

En esta implementación de MongoDB con Sharding, la estrategia de particionamiento utilizada se basa en el uso de una clave shard **hashed**. En particular, todas las colecciones, incluyendo `usuarios`, fueron particionadas utilizando la clave `_id`, la cual se configuró como **hashed**. Este enfoque asegura que los documentos se distribuyan equitativamente entre los shards, aprovechando el balanceo de carga de MongoDB.

El sharding se configuró en tres shards (mongors1, mongors2, y mongors3), cada uno con tres réplicas para garantizar la disponibilidad de los datos y la resistencia ante fallos. El uso de particionamiento hashed distribuye los documentos entre los shards basándose en el hash del valor de la clave shard `_id`.

Esta estrategia es beneficiosa por varias razones:
1. Proporciona una distribución uniforme de los datos, ya que el hash de `_id` tiende a distribuir los documentos de manera equitativa.
2. Evita la necesidad de elegir una clave de particionamiento específica para cada colección, simplificando la configuración.
3. Previene puntos calientes en los shards, ya que los valores hash no siguen ningún patrón predecible.
4. Optimiza la escalabilidad horizontal al permitir que las operaciones de lectura y escritura se distribuyan uniformemente entre los shards.

## Manejo de la Consistencia entre Réplicas

En cuanto a la consistencia entre réplicas, MongoDB implementa un protocolo de consenso llamado **Replica Set**. En cada shard, existe un conjunto de réplicas que contienen copias de los mismos datos. Este sistema asegura la consistencia mediante un **Primary-Secondary Model**, donde solo una instancia actúa como **Primary** y las otras como **Secondaries**.

- **Primary**: Maneja todas las operaciones de escritura.
- **Secondaries**: Replican los datos desde el Primary y pueden ser utilizados para operaciones de lectura si la aplicación lo permite.

En esta implementación, las operaciones de escritura se envían al Primary del conjunto de réplicas de cada shard. MongoDB maneja la replicación de los datos a los nodos secundarios para garantizar la consistencia. Si el Primary falla, uno de los Secondaries es elegido automáticamente como nuevo Primary, asegurando alta disponibilidad.

Se ha configurado un sistema de monitoreo en el que los nodos secundaries verifican periódicamente el estado del Primary y aplican los cambios más recientes para mantener la consistencia.

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

