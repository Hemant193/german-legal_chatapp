import os
from dotenv import load_dotenv
import glob
import uuid
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

load_dotenv()

# Initialize embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Qdrant client
qdrant = QdrantClient(url="http://localhost:6333")
collection_name = "legal_texts"

# Create Qdrant collection
qdrant.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Initialize text splitter
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# Read processed texts
processed_dir = "data/processed"
texts = []
for file_path in glob.glob(os.path.join(processed_dir, "*.txt")):
    with open(file_path, "r", encoding="utf-8") as file:
        texts.append(file.read())

# Split texts into chunks
chunks = []
for text in texts:
    chunks.extend(text_splitter.split_text(text))

# Generate embeddings and store in Qdrant
points = []
for chunk in chunks:
    embedding = embeddings.embed_query(chunk)
    points.append(
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk}
        )
    )

# Upsert points to Qdrant
qdrant.upsert(collection_name=collection_name, points=points)

print(f"Stored {len(points)} text chunks in Qdrant collection '{collection_name}'.")