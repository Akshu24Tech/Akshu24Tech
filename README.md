# Session 3 Assignment: The Memory Vault (Stateful Chatbot)

An interactive, stateful Streamlit chatbot that remembers conversation history across runs using Streamlit's Session State (`st.session_state`) and integrates the Google Gemini API to support dynamic conversations with multiple personalities.

## Features

- **Task 1: Initialize the Memory Vault:** Checks if `"messages"` exists in `st.session_state` and initializes it as an empty list if not.
- **Task 2: Render the Chat History:** Iterates through `st.session_state.messages` to redraw previous messages on the screen using `st.chat_message()`.
- **Task 3: Upgrade the Input UI:** Replaced the old text inputs and buttons with Streamlit's native `st.chat_input()` component using the walrus operator (`:=`).
- **Task 4: Save New Messages to Memory:** Saves user prompts immediately and appends assistant responses returned from the Gemini API to the session state to preserve history.
- **Sidebar Personality Selectbox:** Allows changing chatbot personalities on the fly (e.g., Space Explorer, Shakespearean Bot, Sarcastic Robot) while preserving the conversation history on the screen.

## How to Run

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Google Gemini API key:
   ```bash
   # On Windows (Command Prompt)
   set GOOGLE_API_KEY=your_api_key_here

   # On Windows (PowerShell)
   $env:GOOGLE_API_KEY="your_api_key_here"
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
