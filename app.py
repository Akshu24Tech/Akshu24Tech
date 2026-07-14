import streamlit as st
import google.generativeai as genai
import os

# Initialize the Gemini API Key
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("GOOGLE_API_KEY is not set. Please set the environment variable to use the AI features.")

# Task 1: Initialize the Memory Vault (st.session_state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar settings for chatbot personality
st.sidebar.title("Chatbot Personality")
personality = st.sidebar.selectbox(
    "Choose a persona for your chatbot:",
    ["Friendly Assistant", "Space Explorer", "Shakespearean Bot", "Sarcastic Robot"]
)

personality_instructions = {
    "Friendly Assistant": "You are a helpful and polite AI assistant.",
    "Space Explorer": "You are a space explorer who uses cosmic metaphors and talks about planets, stars, and galaxies.",
    "Shakespearean Bot": "You are a Shakespearean scholar. Speak in Old English, using 'thee', 'thou', 'hath', etc.",
    "Sarcastic Robot": "You are a sarcastic and witty robot. Give humorous, slightly cynical answers."
}

st.title("Multiverse Chatbot 🌌")
st.write("Have a conversation that spans across different personalities in the multiverse!")

# Task 2: Render the Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Task 3: Upgrade the Input UI with native chat_input and walrus operator
if user_message := st.chat_input("Say something..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_message)

    # Prepare chat history for Gemini API (convert to genai role format: user/model)
    gemini_history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    # Task 4: Save User Message to Memory (st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Generate response using Gemini API
    with st.chat_message("assistant"):
        with st.spinner("Tuning into your dimension..."):
            try:
                # Initialize Gemini model with current personality system instruction
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=personality_instructions[personality]
                )
                
                # Start chat with existing history
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(user_message)
                
                # Display assistant response
                st.markdown(response.text)
                
                # Task 4: Save AI Response to Memory (st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Error communicating with Gemini API: {e}")
