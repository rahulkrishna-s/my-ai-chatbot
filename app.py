import streamlit as st
import google.generativeai as genai

st.title("My Gemini Chatbot")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
    st.success("API Key successfully connected!")
except Exception as e:
    st.error("Could not connect to API. Make sure API key is correct.")


user_input = st.chat_input("Ask Gemini something...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(user_input)
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")