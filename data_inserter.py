import json
from pymongo import MongoClient

# Conectar a MongoDB en el contenedor
client = MongoClient('mongodb://127.0.0.1:27017', serverSelectionTimeoutMS=300000, socketTimeoutMS=300000, connectTimeoutMS=300000)
db = client['myTravelDB']

# Funcion para insertar en bloques
def insert_in_batches(collection, data, batch_size=1000):
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        try:
            collection.insert_many(batch)
            print(f"Inserted batch {i // batch_size + 1}")
        except Exception as e:
            print(f"Failed to insert batch {i // batch_size + 1}: {e}")

# Cargar los datos desde los archivos JSON e insertar en bloques
try:
    with open('usuarios.json') as f:
        usuarios = json.load(f)
    insert_in_batches(db.usuarios, usuarios)
    
    with open('posts.json') as f:
        posts = json.load(f)
    insert_in_batches(db.posts, posts)
    
    with open('comentarios.json') as f:
        comentarios = json.load(f)
    insert_in_batches(db.comentarios, comentarios)
    
    with open('likes.json') as f:
        likes = json.load(f)
    insert_in_batches(db.likes, likes)
    
    with open('follows.json') as f:
        follows = json.load(f)
    insert_in_batches(db.follows, follows)

    print("Datos insertados exitosamente.")
except Exception as e:
    print(f"Error durante la inserción: {e}")
