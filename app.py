# app.py
import streamlit as st
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

@st.cache(allow_output_mutation=True)
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

# Load the index and texts
index, text = load_index()
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

st.title("PDF Manual Chatbot")
user_query = st.text_input("Ask me about the manual:")

if user_query:
    manual_response = search_manual(user_query, index, text)
    response = generator(f"Based on the manual: {manual_response}\nUser: {user_query}\nBot:", max_length=100, num_return_sequences=1)
    st.write(f"Bot: {response[0]['generated_text'].strip()}")
