# 🎭 ChronoTales | Multi-Modal Visual Novel Engine
An immersive, choose-your-own-adventure visual novel engine built on Streamlit. By combining Google Gemini's advanced text generation with Pollinations AI's visual asset generation and gTTS (Google Text-to-Speech), this engine converts dry text outputs into fully dynamic, multi-sensory interactive fiction.

This project was built as a Capstone Mini-Project for the **AI Builder** Track at the **MirAI School of Technology**.

---

## ✨ Features
1. **🎭 Stateful AI Narrative:** Using Streamlit session state and Google Gemini's chat capabilities, the app maintains the complete continuity of your adventure.
2. **🔮 Structured JSON Output:** Enforces Gemini to return data matching a strict JSON schema (`story_text`, `image_prompt`, `options`), parsed with robust regex fallbacks.
3. **🎨 Real-Time Visuals:** Converts the AI's descriptive image prompt into a visual scene using the **Pollinations API**, downloading and caching image bytes on the fly.
4. **🔊 Immersive Audio:** Uses **gTTS** to convert the narrative text into dynamic voice narration, rendered in-browser using `st.audio`.
5. **⚡ Dynamic UI:** Dynamically loops through the options lists to render clickable choice buttons, eliminating traditional text inputs.
6. **🛡️ Fault Tolerance:** Designed with defensive `try...except` wrappers and `st.toast` alerts, preventing system crashes if API servers go down.

---

## 🛠️ How to Run

### 1. Install Dependencies
Make sure you have python installed. Run:
```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API Key
You must obtain a Google Gemini API Key. You can set it as an environment variable:

**On Windows (Command Prompt):**
```cmd
set GOOGLE_API_KEY=your_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

*Note: If the environment variable is not set, the app will prompt you with a secure password field in the sidebar to paste your key.*

### 3. Run the Streamlit application
```bash
streamlit run app.py
```

---

## 🏗️ Architectural Concept Walkthrough

- **UI & Caching:** We use `@st.cache_resource` to cache our Gemini client and model instances based on selected Story Settings (Genre and Art Style), reducing startup lag.
- **JSON Engine:** Enforces a clean, structured output from the LLM, enabling the app to programmatically split description text, option lists, and image prompts.
- **Dynamic Buttons:** The game options are generated on the fly inside a loop using custom button event callback states.
- **Graceful Failures:** External integrations (Pollinations, gTTS) are guarded by robust try-catch handlers to alert users with warning toast messages instead of throwing red python tracebacks.
