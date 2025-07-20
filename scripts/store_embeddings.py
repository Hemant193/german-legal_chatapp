import os
import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

# Load from .env
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

PROCESSED_FOLDER = "data/processed"

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS legal_texts (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            embedding VECTOR(384)
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Created legal_texts table (if it didn't exist).")

def store_chunk(text, embedding):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO legal_texts (text, embedding) VALUES (%s, %s)",
        (text, embedding.tolist())  # Convert embedding to list for Pgvector
    )
    conn.commit()
    cursor.close()
    conn.close()

def main():
    """Read all text chunks, generate embeddings, and store them."""
    print("Starting embedding generation...")
    
    create_table()
    
    for filename in os.listdir(PROCESSED_FOLDER):
        if filename.endswith(".txt"):
            file_path = os.path.join(PROCESSED_FOLDER, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
            
            embedding = model.encode(text)
            
            store_chunk(text, embedding)
            print(f"Stored embedding for {filename}")
    
    print("Finished storing all embeddings.")

if __name__ == "__main__":
    main()