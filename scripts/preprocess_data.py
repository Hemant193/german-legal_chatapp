import os

RAW_FOLDER = "data/raw"
PROCESSED_FOLDER = "data/processed"

# Create a folder for Processed file
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)
    print(f"Created folder: {PROCESSED_FOLDER}")

def clean_text(text):
    """Remove extra spaces and newlines from text."""
    text = " ".join(text.split())
    return text

def split_into_chunks(text, chunk_size=500):
    """Split text into chunks of about chunk_size words."""
    words = text.split()
    chunks = []
    current_chunk = []
    word_count = 0

    for word in words:
        current_chunk.append(word)
        word_count += 1
        if word_count >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def process_file(filename):
    """Read, clean, and split a single text file."""
    file_path = os.path.join(RAW_FOLDER, filename)
    with open(file_path, "r", encoding="utf-8") as file:
        raw_text = file.read()
    
    cleaned_text = clean_text(raw_text)
    
    chunks = split_into_chunks(cleaned_text)
    
    base_name = filename.replace(".txt", "")

    for i, chunk in enumerate(chunks):
        chunk_filename = f"{base_name}_chunk_{i}.txt"
        chunk_path = os.path.join(PROCESSED_FOLDER, chunk_filename)
        with open(chunk_path, "w", encoding="utf-8") as file:
            file.write(chunk)
        print(f"Saved: {chunk_path}")

def main():
    """Process all .txt files in the raw folder."""
    print("Starting text processing...")
    for filename in os.listdir(RAW_FOLDER):
        if filename.endswith(".txt"):
            print(f"Processing: {filename}")
            process_file(filename)
    print("Finished processing all files.")

if __name__ == "__main__":
    main()