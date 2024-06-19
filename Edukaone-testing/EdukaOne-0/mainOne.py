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
st.title("‍One: your study companion")

# Define science topics (modify and expand as needed)
science_topics = {
    "Natural Sciences": ["Physics", "Chemistry", "Biology", "Geology", "Astronomy"],
    "Mathematics": ["Calculus", "Algebra", "Geometry", "Statistics"],
}

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role) + f" ({CHARACTER_NAME})"):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("ask One...")

# Recommend topics button
show_recommended_topics = st.button("Recommend Science Topics")

if user_prompt:
    # Add user message and display it
    st.chat_message("user").markdown(user_prompt)

    # **Choose Recommendation Approach:**
    recommended_topics = []

    # Option 1: Recommend based on user prompt (active)
    for category, topics in science_topics.items():
        for topic in topics:
            if topic.lower() in user_prompt.lower():
                recommended_topics.append(f"{category}: {topic}")

    # Option 2: Machine Learning-Based Recommendation (future implementation)
    # user_prompt_with_recommendation_request = f"{user_prompt} Can you also recommend some related topics?"

    if show_recommended_topics:
        # Only recommend if the button is clicked
        # Display recommendations (using filtered_recommendations if applicable)
        if recommended_topics:
            st.write("Hey! Here are some related science topics you might be interested in:")
            for topic in recommended_topics:
                st.write(f"- {topic}")
        else:
            st.write("No science topics found related to your prompt yet. Try a broader search!")

    # Send user prompt to Gemini-Pro (unchanged)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro response (unchanged)
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
