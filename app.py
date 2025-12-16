import streamlit as st

st.title("My AI Chatbot")
st.write("Streamlit is running.")

user_input = st.chat_input("Say something:")
if user_input:
    st.write(f"You said: {user_input}")