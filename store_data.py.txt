# store_data.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def index_text(text_file_path):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    with open(text_file_path, "r") as file:
        text = file.read().split('.')
    embeddings = model.encode(text)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, text

if __name__ == "__main__":
    text_file_path = "manual_text.txt"
    index, text = index_text(text_file_path)
    faiss.write_index(index, "manual_index.faiss")
    with open("manual_sentences.txt", "w") as file:
        file.write("\n".join(text))
