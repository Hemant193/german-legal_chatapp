from dotenv import load_dotenv
import os
import psycopg2
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct


load_dotenv()


conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cursor = conn.cursor()


qdrant = QdrantClient(url="http://localhost:6333")


collection_name = "legal_texts"
qdrant.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)


cursor.execute("SELECT id, text, embedding FROM legal_texts")
rows = cursor.fetchall()


points = []
for row in rows:
    id, text, embedding = row
    embedding = eval(embedding) if isinstance(embedding, str) else embedding
    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": text}
        )
    )


qdrant.upsert(collection_name=collection_name, points=points)

cursor.close()
conn.close()
print(f"Migrated {len(points)} texts to Qdrant collection '{collection_name}'.")