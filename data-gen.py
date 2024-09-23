from pymongo import MongoClient
from faker import Faker
import random

client = MongoClient("mongodb://localhost:27029")  # Conexión al router mongos
db = client.travelSocialDB

fake = Faker()

# Generar 5000 usuarios
users = []
for _ in range(5000):
    users.append({
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(),
        "bio": fake.text()
    })
db.users.insert_many(users)

# Generar 10,000 posts
posts = []
for _ in range(10000):
    posts.append({
        "user_id": random.choice(users)['_id'],
        "content": fake.text(),
        "image_links": [fake.image_url() for _ in range(random.randint(1, 5))],
        "date": fake.date_time()
    })
db.posts.insert_many(posts)

# Generar 50,000 comentarios
comments = []
for _ in range(50000):
    comments.append({
        "post_id": random.choice(posts)['_id'],
        "user_id": random.choice(users)['_id'],
        "comment": fake.text(),
        "date": fake.date_time()
    })
db.comments.insert_many(comments)

# Generar 100,000 likes
likes = []
for _ in range(100000):
    likes.append({
        "post_id": random.choice(posts)['_id'],
        "user_id": random.choice(users)['_id']
    })
db.likes.insert_many(likes)
