from PIL import Image
import streamlit as st
import numpy as np
import pickle

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
    loaded_data = pickle.load(input_file)

# User input section
user_input = st.text_input(
    label="User Input", label_visibility="hidden", placeholder="Enter your question..."
)

if user_input:
    # Process user input (logic for generating response)
    response = f"Bot response to: {user_input}"
    st.text(response)
