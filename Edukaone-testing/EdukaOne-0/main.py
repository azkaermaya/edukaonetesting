import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Welcome to EdukaOne",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Character Persona
CHARACTER_NAME = "One"
CHARACTER_DESCRIPTION = "a clever and friendly assistant who works for EdukaOne. One is a genius scientist who loves teaching every student about science!"

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    intro_message = f"I'm {CHARACTER_NAME}, {CHARACTER_DESCRIPTION}"
    st.session_state.chat_session.send_message(intro_message)

# Display the chatbot's title on the page
st.title("🧑‍🚀One: your study companion")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role) + f" ({CHARACTER_NAME})"):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("ask One...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
