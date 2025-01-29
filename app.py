# app.py
import streamlit as st
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

@st.cache(allow_output_mutation=True)
def load_index(index_file, sentences_file):
    index = faiss.read_index(index_file)
    with open(sentences_file, "r") as file:
        text = file.read().split('\n')
    return index, text

def search_manual(query, index, text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)
    return text[I[0][0]]

st.title("PDF Manual Chatbot")

uploaded_index_file = st.file_uploader("Upload manual_index.faiss", type=["faiss"])
uploaded_sentences_file = st.file_uploader("Upload manual_sentences.txt", type=["txt"])

if uploaded_index_file and uploaded_sentences_file:
    with open("manual_index.faiss", "wb") as f:
        f.write(uploaded_index_file.getbuffer())
    with open("manual_sentences.txt", "wb") as f:
        f.write(uploaded_sentences_file.getbuffer())
    index, text = load_index("manual_index.faiss", "manual_sentences.txt")
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')

    user_query = st.text_input("Ask me about the manual:")

    if user_query:
        manual_response = search_manual(user_query, index, text)
        response = generator(f"Based on the manual: {manual_response}\nUser: {user_query}\nBot:", max_length=100, num_return_sequences=1)
        st.write(f"Bot: {response[0]['generated_text'].strip()}")

