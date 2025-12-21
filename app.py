import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GuessWho AI")
st.title("GuessWho - AI Guessing Game")

# Game settings
MAX_QUESTIONS = 20

system_prompt = """
You are a 'GuessWho' game master (like Akinator). 
1. The user is thinking of a famous person, fictional character, or animal.
2. Your goal is to guess who it is by asking one 'Yes/No' question at a time.
3. Keep track of the user's answers to narrow down the possibilities.
4. When you are 90% sure, make a guess like: 'Are you thinking of [Name]?'
5. If you guess wrong, keep asking more questions!
6. When the user says they're ready, ask your first question immediately.
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
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Sidebar
with st.sidebar:
    st.header("Game Controls")
    if st.button("New Game", use_container_width=True):
        st.session_state.messages = []
        st.session_state.game_started = False
        st.session_state.game_over = False
        st.rerun()
    
    st.divider()
    st.subheader("Stats")
    question_count = len([msg for msg in st.session_state.messages if msg["role"] == "model"])
    st.metric("Questions Asked", f"{question_count}/{MAX_QUESTIONS}")

# Greeting when user first arrives
if not st.session_state.game_started and len(st.session_state.messages) == 0:
    st.chat_message("assistant").write(
        "Hey! I'm **GuessWho AI**, your AI-powered guessing game master!\n\n"
        "Think of any **famous person**, **fictional character**, or **animal**, "
        f"and I'll try to guess who it is in **{MAX_QUESTIONS} questions** or less.\n\n"
        "Ready to challenge me?"
    )
    
    if st.button("I'm Ready!", use_container_width=True, type="primary"):
        st.session_state.game_started = True
        with st.spinner("Let the game begin..."):
            try:
                response = model.generate_content("The user is ready. Ask your first question.")
                st.session_state.messages.append({"role": "model", "parts": [response.text]})
                st.rerun()
            except Exception as e:
                st.error(f"Could not start game: {e}")
    
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["parts"][0])

# Game over logic 
question_count = len([msg for msg in st.session_state.messages if msg["role"] == "model"])
if question_count >= MAX_QUESTIONS and not st.session_state.game_over:
    st.session_state.game_over = True
    st.rerun()

if st.session_state.game_over:
    st.write("---")
    st.snow()
    st.error(f"**You stumped me!** I couldn't guess it in {MAX_QUESTIONS} questions.")
    
    # Ask user to reveal who they were thinking of
    with st.form("reveal_form"):
        st.write("**Who were you thinking of?**")
        answer = st.text_input("Tell me who it was:")
        if st.form_submit_button("Reveal"):
            if answer:
                st.info(f"Ah, **{answer}**! I'll remember that for next time.")
                st.balloons()
    
    if st.button("Play Again", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.game_started = False
        st.session_state.game_over = False
        st.rerun()
    
    st.stop()  

# Response buttons
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

# Final input handling
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
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")