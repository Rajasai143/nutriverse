import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()

# Configure the Google Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to create a Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="Recipe Generator AI", layout="wide")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# local_css("styles1.css")

st.header("Recipe Generator AI")

# Initialize the session state for the chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Text area for user input
input = st.text_area("Enter the ingredients you have:", key="input")

# Button to submit the ingredients
submit = st.button("Generate Recipe")

if submit and input:
    prompt = f"Generate a recipe using the following ingredients: {input}"
    response = get_gemini_response(prompt)
    # Add user query and response to session chat history
    st.session_state["chat_history"].append(("You", input))
    
    st.subheader("Generated Recipe:")
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    st.markdown(f'<div class="response">{response_text}</div>', unsafe_allow_html=True)
    st.session_state["chat_history"].append(("Bot", response_text))

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state["chat_history"]:
    if role == "Bot":
        st.markdown(f"**{role}:** {text}")
    else:
        st.write(f"{role}: {text}")
