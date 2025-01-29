# chatbot.py
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def load_index():
    index = faiss.read_index("manual_index.faiss")
    with open("manual_sentences.txt", "r") as file:
        text = file.read().split('\n')
    return index, text

def search_manual(query, index, text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)
    return text[I[0][0]]

if __name__ == "__main__":
    index, text = load_index()
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

    while True:
        query = input("User: ")
        manual_response = search_manual(query, index, text)
        response = generator(f"Based on the manual: {manual_response}\nUser: {query}\nBot:", max_length=100, num_return_sequences=1)
        print(f"Bot: {response[0]['generated_text'].strip()}")
