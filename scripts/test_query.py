from dotenv import load_dotenv
import os
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline
from qdrant_client import QdrantClient

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

en_to_de = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de", device="mps")
de_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en", device="mps")


qdrant_client = QdrantClient(url="http://localhost:6333")

def query_legal_texts(query, k=3):
    """Query the Qdrant legal_texts collection for top-k relevant texts and translate to English."""
    translated_query = en_to_de(query)[0]["translation_text"]
    print(f"Translated query (English to German): {translated_query}")

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name="legal_texts",
        embedding=embeddings
    )

    results = vector_store.similarity_search(translated_query, k=k)

    print("\nTop relevant texts (translated to English):")
    for i, doc in enumerate(results, 1):
        translated_text = de_to_en(doc.page_content[:1000])[0]["translation_text"]
        print(f"\nResult {i}:")
        print(translated_text[:200] + "...")

def main():
    print("German Legal Query Backend")
    query = input("Enter your query in English (e.g., 'What are the requirements for a residence permit in Germany?'): ")
    if query:
        query_legal_texts(query)
    else:
        print("No query provided.")

if __name__ == "__main__":
    main()