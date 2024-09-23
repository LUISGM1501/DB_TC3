import json
from pymongo import MongoClient

# Conectar a MongoDB en el contenedor
client = MongoClient('mongodb://172.25.0.14:27017', serverSelectionTimeoutMS=60000, socketTimeoutMS=60000)

# Seleccionar la base de datos y las colecciones
db = client['myTravelDB']

# Cargar los datos desde los archivos JSON
with open('usuarios.json') as f:
    usuarios = json.load(f)

with open('posts.json') as f:
    posts = json.load(f)

with open('comentarios.json') as f:
    comentarios = json.load(f)

with open('likes.json') as f:
    likes = json.load(f)

with open('follows.json') as f:
    follows = json.load(f)

# Insertar los datos en las colecciones correspondientes
db.usuarios.insert_many(usuarios)
db.posts.insert_many(posts)
db.comentarios.insert_many(comentarios)
db.likes.insert_many(likes)
db.follows.insert_many(follows)

print("Datos insertados exitosamente.")
