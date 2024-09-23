import json
import random
from faker import Faker

fake = Faker()

# Generar 5000 usuarios
usuarios = []
for i in range(5000):
    usuarios.append({
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
        "bio": fake.text(max_nb_chars=200)
    })

# Generar 10,000 posts
posts = []
for i in range(10000):
    posts.append({
        "user": random.choice(usuarios)["username"],
        "content": fake.text(max_nb_chars=500),
        "photos": [fake.image_url() for _ in range(random.randint(1, 3))],
        "published_date": fake.date_time_this_year().isoformat()
    })

# Generar 50,000 comentarios
comentarios = []
for i in range(50000):
    comentarios.append({
        "user": random.choice(usuarios)["username"],
        "content": fake.text(max_nb_chars=300),
        "published_date": fake.date_time_this_year().isoformat(),
        "post": random.choice(posts)["content"]
    })

# Generar 100,000 likes
likes = []
for i in range(100000):
    likes.append({
        "user": random.choice(usuarios)["username"],
        "post": random.choice(posts)["content"]
    })

# Generar 20,000 follows
follows = []
for i in range(20000):
    follower = random.choice(usuarios)["username"]
    followee = random.choice(usuarios)["username"]
    # Evitar que un usuario se siga a sí mismo
    while follower == followee:
        followee = random.choice(usuarios)["username"]
    follows.append({
        "follower": follower,
        "followee": followee
    })

# Guardar en archivos JSON
with open('usuarios.json', 'w') as f:
    json.dump(usuarios, f)

with open('posts.json', 'w') as f:
    json.dump(posts, f)

with open('comentarios.json', 'w') as f:
    json.dump(comentarios, f)

with open('likes.json', 'w') as f:
    json.dump(likes, f)

with open('follows.json', 'w') as f:
    json.dump(follows, f)

print("Archivos generados exitosamente.")
