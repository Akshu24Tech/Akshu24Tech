import streamlit as st
import google.generativeai as genai
import os
import json
import urllib.parse
import requests
import tempfile
from gtts import gTTS

# Configure Streamlit page for a premium visual novel experience
st.set_page_config(
    page_title="ChronoTales | Interactive Multi-Modal Visual Novel Engine",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics, glassmorphism, responsive visual novel cards, and custom buttons
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Main elements styling */
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #a29bfe 10%, #6c5ce7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .sub-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        text-align: center;
        color: #b2bec3;
        margin-bottom: 25px;
    }
    
    /* Glassmorphism card for story text */
    .narrative-card {
        background: rgba(26, 26, 36, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    
    .narrative-text {
        font-family: 'Inter', sans-serif;
        color: #f5f6fa;
        font-size: 1.15rem;
        line-height: 1.7;
    }
    
    /* Custom style for interactive choices buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #6c5ce7 0%, #4834d4 100%);
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 14px 20px;
        width: 100%;
        margin-bottom: 12px;
        text-align: left;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.2);
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #863ffc 0%, #6c5ce7 100%);
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.4);
        transform: translateY(-2px);
        color: #ffffff !important;
    }
    
    div.stButton > button:active {
        transform: translateY(0);
    }
    
    /* Custom styling for visuals container */
    .stImage > img {
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.3s ease;
    }
    
    .stImage > img:hover {
        transform: scale(1.01);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- PHASE 1: The Director's Cut (UI & Configuration) -----------------

# Securely cache the Gemini configuration using Streamlit's resource cache
@st.cache_resource
def get_generative_model(api_key, system_instruction):
    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash as the fast, JSON-capable model for real-time narrative generation
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction,
        generation_config={"response_mime_type": "application/json"}
    )
    return model

# Set up Sidebar settings
st.sidebar.title("🛠️ Story Settings")

genre = st.sidebar.selectbox(
    "Choose Story Genre:",
    ["Fantasy", "Sci-Fi", "Mystery", "Horror", "Cyberpunk", "Slice of Life", "Medieval Fantasy"]
)

art_style = st.sidebar.selectbox(
    "Choose Art Style:",
    ["Anime Illustration", "Cinematic 3D Render", "Pixel Art", "Dreamy Watercolor", "Dark Fantasy Painting", "Neon Cyberpunk Art"]
)

# API Key check and sidebar input fallback
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

# Clean up helper for audio files to avoid disk overflow
def clean_up_old_audio():
    if "current_scene" in st.session_state and st.session_state.current_scene:
        old_path = st.session_state.current_scene.get("audio_path")
        if old_path and os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception:
                pass

# Game reset button in sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset / Restart Adventure"):
    clean_up_old_audio()
    st.session_state.story_history = []
    st.session_state.current_scene = None
    st.session_state.gemini_chat = None
    st.rerun()

# Automatically restart if Story settings change, to keep visual style and narrative aligned
if "genre" not in st.session_state:
    st.session_state.genre = genre
if "art_style" not in st.session_state:
    st.session_state.art_style = art_style

if st.session_state.genre != genre or st.session_state.art_style != art_style:
    clean_up_old_audio()
    st.session_state.genre = genre
    st.session_state.art_style = art_style
    st.session_state.story_history = []
    st.session_state.current_scene = None
    st.session_state.gemini_chat = None

# Initialize state history and engine
if "story_history" not in st.session_state:
    st.session_state.story_history = []
if "current_scene" not in st.session_state:
    st.session_state.current_scene = None
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None


# ----------------- PHASE 2: The Structured JSON Engine -----------------

# Define a dynamic system prompt based on user settings to enforce structured JSON output
def get_system_prompt(selected_genre, selected_style):
    return f"""You are the director and narrator of an interactive "Choose Your Own Adventure" visual novel.
The genre of the story is: {selected_genre}
The art style of the story is: {selected_style}

You must strictly output all responses as a single, valid JSON object. Do not include markdown codeblocks (like ```json) or any prefix/suffix text. Output ONLY raw JSON.

The JSON object must contain exactly these three keys:
1. "story_text": A compelling, highly descriptive paragraph (3-4 sentences) narrating the current scene or the consequences of the user's action in a vivid, narrative style. Write in the second person ("You...").
2. "image_prompt": A highly detailed and descriptive prompt for an image generation API (Pollinations) that depicts the current scene. It must start with the art style name "{selected_style}" and describe the characters, environment, lighting, and mood (e.g., "{selected_style}, a mysterious hooded figure sitting in a dark tavern, warm candle light, detailed digital art"). Avoid using generic terms, specify details. Do not use negative words.
3. "options": A list containing 2 to 3 distinct, interesting choices (strings) representing the user's next possible actions. Keep choices short and action-oriented.

Example JSON output structure:
{{
  "story_text": "The massive iron gates creaked open, revealing a cobblestone path engulfed in a thick, silver mist. Ahead, the silhouette of a forgotten manor loomed against the pale moonlight. A distant owl hooted, warning you of the secrets that sleep within.",
  "image_prompt": "{selected_style}, a spooky gothic manor at night under a full moon, dark silver fog rolling across the ground, detailed digital painting, high resolution",
  "options": [
    "Follow the cobblestone path toward the manor's front door.",
    "Investigate the overgrown hedge maze to the left.",
    "Wait by the gates to see if anyone is following you."
  ]
}}
"""

def parse_gemini_json(response_text):
    clean_text = response_text.strip()
    # Strip markdown backticks if returned despite system instructions
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    clean_text = clean_text.strip()
    
    # Try a direct parse
    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        # Fallback: attempt regex extraction of the JSON block
        import re
        match = re.search(r"\{.*\}", clean_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise

def sanitize_scene_data(data):
    if not isinstance(data, dict):
        data = {}
    return {
        "story_text": data.get("story_text", "The story unfolds, but the details are lost in the mist..."),
        "image_prompt": data.get("image_prompt", f"{art_style}, mysterious atmospheric background"),
        "options": data.get("options", ["Continue forward", "Look around", "Go back"])[:3] # Max 3 options
    }


# ----------------- PHASE 4: Multi-Media Rendering & TTS & PHASE 5: Graceful Failures -----------------

def fetch_pollinations_image(prompt):
    # Process and encode prompt safely for GET request
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=42"
    
    try:
        # Phase 5: Try...except block to handle API / Network issues gracefully
        response = requests.get(url, timeout=12)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        # Use Streamlit's toast notification on failure
        st.toast("🎨 Image server is busy, skipping visual...", icon="⚠️")
    return None

def generate_tts_audio(text):
    try:
        # Phase 5: Try...except block for Text-to-Speech generation
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_path = temp_file.name
        temp_file.close() # Close handle so gTTS library can safely write
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_path)
        return temp_path
    except Exception as e:
        st.toast("🔊 Narration engine failed, playing without sound.", icon="⚠️")
        return None


# ----------------- UI rendering and gameplay state controller -----------------

# Page Titles
st.markdown("<h1 class='main-title'>🎭 ChronoTales</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Interactive Multi-Modal Choose-Your-Own-Adventure Engine</div>", unsafe_allow_html=True)

# Main gameplay logic
if api_key:
    system_instruction = get_system_prompt(genre, art_style)
    
    # Initialize game if not already running
    if st.session_state.current_scene is None or st.session_state.gemini_chat is None:
        with st.spinner("🔮 Constructing the opening scene..."):
            try:
                # Cache-instantiate model based on settings
                model = get_generative_model(api_key, system_instruction)
                st.session_state.gemini_chat = model.start_chat(history=[])
                
                # Request introduction
                response = st.session_state.gemini_chat.send_message(
                    f"Start the adventure. Create the opening scene in the {genre} genre."
                )
                
                raw_data = parse_gemini_json(response.text)
                scene = sanitize_scene_data(raw_data)
                
                # Fetch assets
                scene["image_bytes"] = fetch_pollinations_image(scene["image_prompt"])
                scene["audio_path"] = generate_tts_audio(scene["story_text"])
                
                st.session_state.current_scene = scene
            except Exception as e:
                st.error(f"🚨 Failed to load story: {e}. Please check your API Key and connection.")

    # Handler for choice selection (Phase 3 button callbacks)
    def handle_choice(selected_option):
        clean_up_old_audio()
        
        # Save previous scene state to history log
        if st.session_state.current_scene:
            st.session_state.story_history.append({
                "story_text": st.session_state.current_scene["story_text"],
                "image_bytes": st.session_state.current_scene.get("image_bytes"),
                "choice_made": selected_option
            })
            
        with st.spinner("🔮 Shaping reality..."):
            try:
                # Phase 5: Error check the Gemini chat message cycle
                response = st.session_state.gemini_chat.send_message(selected_option)
                raw_data = parse_gemini_json(response.text)
                scene = sanitize_scene_data(raw_data)
                
                # Fetch assets
                scene["image_bytes"] = fetch_pollinations_image(scene["image_prompt"])
                scene["audio_path"] = generate_tts_audio(scene["story_text"])
                
                st.session_state.current_scene = scene
            except Exception as e:
                st.error(f"🚨 The story threads have tangled: {e}. Attempting recovery...")
    
    # Render the active scene
    if st.session_state.current_scene:
        active_scene = st.session_state.current_scene
        
        # Split layout for immersive Visual Novel vibe: Visual on left, narrative on right
        col1, col2 = st.columns([5, 6], gap="large")
        
        with col1:
            if "image_bytes" in active_scene and active_scene["image_bytes"]:
                st.image(active_scene["image_bytes"], use_container_width=True)
            else:
                # Fallback design if API goes down
                st.info("🌌 The screen remains dark, but the whispers continue...")
                st.markdown(
                    f"""
                    <div style='background-color:#1e2030; border-radius:16px; height:400px; display:flex; align-items:center; justify-content:center; border:1px dashed #4834d4;'>
                        <p style='color:#a29bfe; font-family:Inter; text-align:center;'>Visual temporarily lost in the void.<br>Style: {art_style}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
        with col2:
            st.markdown(
                f"""
                <div class="narrative-card">
                    <p class="narrative-text">{active_scene["story_text"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Narration Player
            if "audio_path" in active_scene and active_scene["audio_path"] and os.path.exists(active_scene["audio_path"]):
                st.audio(active_scene["audio_path"], format="audio/mp3")
                
            st.markdown("### Choose Your Next Action:")
            
            # ----------------- PHASE 3: Dynamic UI Generation -----------------
            # Write a for loop that iterates over the options list to dynamically render st.button()
            options = active_scene.get("options", [])
            for idx, option in enumerate(options):
                # Trigger handle_choice with the selected choice text using on_click argument
                st.button(
                    option,
                    key=f"choice_btn_{idx}_{len(st.session_state.story_history)}",
                    on_click=handle_choice,
                    args=(option,)
                )

    # Historical Story log
    if st.session_state.story_history:
        st.markdown("---")
        with st.expander("📖 Read Your Adventure Log So Far"):
            for step, hist in enumerate(st.session_state.story_history):
                step_col1, step_col2 = st.columns([2, 8])
                with step_col1:
                    if hist.get("image_bytes"):
                        st.image(hist["image_bytes"], use_container_width=True)
                with step_col2:
                    st.markdown(f"**Scene {step + 1}**")
                    st.write(hist["story_text"])
                    st.markdown(f"**Your Choice:** *{hist['choice_made']}*")
                st.divider()

else:
    # Setup guidance screen for entering key
    st.info("👋 Welcome, Adventurer! Let's build your story.")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            f"""
            ### To start your journey:
            1. **Provide a Google Gemini API Key** in the sidebar.
            2. Choose your narrative **Genre** (e.g., *Cyberpunk*, *Fantasy*).
            3. Choose the **Art Style** for the visual generators.
            4. The engine will automatically generate the opening scene!
            
            ### Concepts demonstrated:
            - **Stateful Chat Engine**: Maintains the context of your choices.
            - **Structured JSON Parsing**: Model strictly outputs structured data.
            - **Dynamic UI**: Action choices dynamically morph based on the AI's output.
            - **TTS Integration**: Every scene text is read aloud dynamically.
            """
        )
    with col2:
        # A nice visual mock using pollinations or static illustration
        st.markdown(
            """
            <div style='background-color:#1e2030; border-radius:16px; height:320px; display:flex; align-items:center; justify-content:center; border:1px solid rgba(255,255,255,0.05); box-shadow:0 8px 32px rgba(0,0,0,0.3);'>
                <div style='text-align:center; padding: 20px;'>
                    <h2 style='font-family:Outfit; color:#a29bfe; font-size:1.8rem; margin-bottom:10px;'>🔮 Visual Novel Awaiting Key</h2>
                    <p style='color:#b2bec3; font-family:Inter;'>Please input your API key to let the storytelling begin.</p>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
