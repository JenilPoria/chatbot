import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variable
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chatbot with Groq",
    page_icon=":brain:",  # favicon emoji
    layout="centered",  # page layout screen
)

# Setup Groq AI model
chat = ChatGroq(api_key=GROQ_API_KEY, temperature=0,model="llama-3.3-70b-versatile")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Function to translate roles between Groq and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Display the chatbot's title on the page
st.title("Groq Chatbot")

# Display the chat history
for message in st.session_state.history:
    with st.chat_message(translate_role_for_streamlit(message["role"])):
        st.markdown(message["text"])

# Input field for user's message
user_prompt = st.chat_input("Ask Groq Model...")

if user_prompt:
    with st.spinner("Thinking..."):
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send the user's message to Groq and get the response
        groq_response = chat.predict(user_prompt)  # Using predict() instead of run()

        # Add the response to history
        st.session_state.history.append({"role": "assistant", "text": groq_response})

        # Display Groq's response
        with st.chat_message("assistant"):
            st.markdown(groq_response)
