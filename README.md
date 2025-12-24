# GuessWho AI - Powered by Gemini

## About The Project
This is a logic based guessing game where the AI acts as the Game Master (similar to Akinator). It challenges the user to think of a character, and the AI attempts to guess it using a limited number of Yes/No questions.

Built to explore **State Management** in Streamlit and **System Prompting** with Large Language Model API.

### Tech Stack
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)
![Gemini API](https://img.shields.io/badge/AI-Gemini%20Flash-green)

## How It Works
The core challenge was handling Streamlit's rerun cycle while maintaining conversation history.
1. **Session State:** I used `st.session_state` to persist the chat history and the `game_started` status across UI updates.
2. **System Prompting:** Used system prompt of gemini api to make sure the ai have the GuessWho-ai persona and follows rules of the game.
3. **API Integration:** Connects to Google's Gemini Flash model for low-latency responses(If you use the free gemini api, the request per day available can be low and it can be hard to play many turns).

## How to Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/rahulkrishna-s/guesswho-ai.git
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
3. **Add your API Key:** Create a .streamlit/secrets.toml file and add:
    ```bash
    GOOGLE_API_KEY = "your_key_here"
4. **Run the App**
    ```bash
    streamlit run app.py