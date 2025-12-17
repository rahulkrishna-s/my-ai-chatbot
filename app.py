import streamlit as st
import google.generativeai as genai

st.title("My Gemini Chatbot")

system_prompt = """
You are a 'Guess Who' game master (like Akinator). 
1. The user is thinking of a famous person, fictional character, or animal.
2. Your goal is to guess who it is by asking one 'Yes/No' question at a time.
3. Keep track of the user's answers to narrow down the possibilities.
4. When you are 90% sure, make a guess like: 'Are you thinking of [Name]?'
5. If you guess wrong, keep asking more questions!
6. Start by introducing yourself and asking the user to think of someone.
"""

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)
    st.success("API Key successfully connected!")
except Exception as e:
    st.error("Could not connect to API. Make sure API key is correct.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["parts"][0])


user_input = st.chat_input("Ask Gemini something...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({"role": "user", "parts": [user_input]})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(st.session_state.messages)
                st.write(response.text)
                st.session_state.messages.append({"role": "model", "parts": [response.text]})
            except Exception as e:
                st.error(f"An error occurred: {e}")