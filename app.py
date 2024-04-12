from PIL import Image
import streamlit as st
import numpy as np
import pickle

from src.llm_bot import LocalRAGllm

st.title("IPL 2024 Auction - Q&A")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

_img = "./data/ipl_2024.webp"
image = Image.open(_img)
st.image(image, use_column_width="auto")

# Load the pickled news article list
with open("./data/ipl_2024_auction_news_article.pkl", "rb") as input_file:
    # Unpickle the data object
    news_articles = pickle.load(input_file)

rag_chain = LocalRAGllm(
    llm_model_name="google/flan-t5-small",
    llm_model_type="text2text-generation",
    llm_max_length=1000,
    embedding_model_name="BAAI/bge-base-en-v1.5",
    chunk_size=512,
    documents=news_articles,
)

# User input section
user_input = st.text_input(
    label="User Input", label_visibility="hidden", placeholder="Enter your question..."
)

if user_input:
    # Process user input (logic for generating response)
    response = rag_chain(user_question=user_input)
    st.text(response)
