import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GuessWho AI")
st.title("GuessWho - AI Guessing Game")

system_prompt = """
You are a 'Guess Who' game master (like Akinator). 
1. The user is thinking of a famous person, fictional character, or animal.
2. Your goal is to guess who it is by asking one 'Yes/No' question at a time.
3. Keep track of the user's answers to narrow down the possibilities.
4. When you are 90% sure, make a guess like: 'Are you thinking of [Name]?'
5. If you guess wrong, keep asking more questions!
6. Start by introducing yourself and asking the user to think of someone.
"""

# API config
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)
except Exception as e:
    st.error("Could not connect to API. Make sure API key is correct.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Game Controls")
    if st.button("New Game", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("Stats")
    question_count = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
    st.metric("Questions Asked", question_count)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["parts"][0])

st.write("---")
cols = st.columns(5)
user_answer = None

with cols[0]:
    if st.button("Yes", use_container_width=True):
        user_answer = "Yes"
with cols[1]:
    if st.button("No", use_container_width=True):
        user_answer = "No"
with cols[2]:
    if st.button("Don't Know", use_container_width=True):
        user_answer = "I don't know"
with cols[3]:
    if st.button("Probably", use_container_width=True):
        user_answer = "Probably"
with cols[4]:
    if st.button("Probably Not", use_container_width=True):
        user_answer = "Probably not"

#final input handling
if user_answer:
    final_input = user_answer
else:
    final_input = st.chat_input("Or type your answer here...")

if final_input:
    with st.chat_message("user"):
        st.write(final_input)

    st.session_state.messages.append({"role": "user", "parts": [final_input]})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(st.session_state.messages)
                st.write(response.text)
                st.session_state.messages.append({"role": "model", "parts": [response.text]})
                st.rerun() # Rerun to clear the button state
            except Exception as e:
                st.error(f"An error occurred: {e}")