import streamlit as st
import requests
import urllib.parse
import random

# Set page configuration for a premium look
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and modern typography
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;600&display=swap');
        
        /* Font styling */
        html, body, [class*="css"], .stApp {
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3, .title-text {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
        }

        /* Animated Title Gradient */
        .title-container {
            background: linear-gradient(135deg, #FF3366 0%, #9933FF 50%, #33CCFF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            animation: gradient-shift 8s ease infinite;
            background-size: 200% 200%;
        }

        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .subtitle-text {
            color: #888899;
            font-size: 1.15rem;
            margin-bottom: 2rem;
            font-weight: 300;
        }

        /* Card and Panel Styling */
        div[data-testid="stSidebar"] {
            background-color: #0E0F14 !important;
            border-right: 1px solid #1F2029;
        }

        /* Customize buttons */
        div.stButton > button {
            border-radius: 12px !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            padding: 0.6rem 1.8rem !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            border: none !important;
            cursor: pointer;
        }

        /* Custom generate button style (Vibrant purple-pink gradient) */
        div.stButton > button[key="generate_button"] {
            background: linear-gradient(135deg, #7F00FF 0%, #FF007F 100%) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(127, 0, 255, 0.4) !important;
        }

        div.stButton > button[key="generate_button"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(127, 0, 255, 0.6) !important;
            background: linear-gradient(135deg, #8E2DE2 0%, #F000FF 100%) !important;
        }

        /* Custom surprise button style (Glassmorphic dark button) */
        div.stButton > button[key="surprise_button"] {
            background-color: #1E1F29 !important;
            color: #D1D2D9 !important;
            border: 1px solid #3E4059 !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        }

        div.stButton > button[key="surprise_button"]:hover {
            color: #FFFFFF !important;
            border-color: #FF007F !important;
            box-shadow: 0 0 12px rgba(255, 0, 127, 0.5) !important;
            transform: translateY(-2px) !important;
        }

        /* Download button styling */
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.8rem !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(0, 198, 255, 0.4) !important;
            transition: all 0.3s ease !important;
        }

        div.stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 198, 255, 0.6) !important;
        }

        /* Image Display container */
        .image-card {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid #2A2B36;
            margin-top: 1.5rem;
            background-color: #12131C;
        }
    </style>
""", unsafe_allow_html=True)

# Main UI layout
st.markdown('<div class="title-container">AI Image Studio 🎨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Transform your thoughts into stunning, high-resolution digital art instantly.</div>', unsafe_allow_html=True)

# Task 4: Surprise Me! Prompts list
creative_prompts = [
    "An astronaut riding a horse on Mars, high detail digital art",
    "A cyberpunk street food vendor in Tokyo, neon signs, rain reflection, unreal engine 5",
    "A cozy cabin in a glowing bioluminescent forest, aurora borealis, fantasy concept art",
    "A futuristic city built inside a giant crystal cavern, flying vehicles, retro-futurism",
    "A majestic ancient dragon perched on top of a futuristic neo-noir skyscraper"
]

# Initialize st.session_state variables for prompt control
if "prompt_val" not in st.session_state:
    st.session_state.prompt_val = ""
if "trigger_gen" not in st.session_state:
    st.session_state.trigger_gen = False

# Sidebar Configuration Panel
st.sidebar.markdown("### ⚙️ Studio Settings")

art_style = st.sidebar.selectbox(
    "Art Style",
    ["Cinematic", "Anime", "3D Render", "Oil Painting", "Digital Art", "Cyberpunk", "Sketch", "Pixel Art"]
)

# Resolution Settings
st.sidebar.markdown("---")
st.sidebar.markdown("📐 Image Dimensions")
width = st.sidebar.slider("Width (px)", min_value=256, max_value=1280, value=768, step=64)
height = st.sidebar.slider("Height (px)", min_value=256, max_value=1280, value=768, step=64)

# Task 3: Magic Enhance Toggle in sidebar
st.sidebar.markdown("---")
magic_enhance = st.sidebar.checkbox("  Enable Magic Enhance", value=False)

if magic_enhance:
    st.sidebar.info("💡 Magic Enhance: High-quality descriptors will be secretly added to boost prompt results.")

# Main Input Bar
prompt = st.text_input(
    "What masterpiece do you want to generate?",
    value=st.session_state.prompt_val,
    placeholder="Describe your creative vision in detail..."
)

# Action Buttons layout
col1, col2, _ = st.columns([1.5, 1.5, 7])

with col1:
    generate_btn = st.button("🚀 Generate Art", key="generate_button", use_container_width=True)

with col2:
    surprise_btn = st.button("  Surprise Me!", key="surprise_button", use_container_width=True)

# Task 4: Surprise Me! Logic
if surprise_btn:
    # Pick a random creative prompt
    st.session_state.prompt_val = random.choice(creative_prompts)
    st.session_state.trigger_gen = True
    st.rerun()

# Execute generation if the user clicked "Generate Art" OR if "Surprise Me!" triggered it
should_generate = generate_btn or st.session_state.trigger_gen

if should_generate:
    # Reset trigger gen state for the next run
    st.session_state.trigger_gen = False
    
    # Use prompt value from session state if trigger_gen was active, otherwise use the text input
    active_prompt = st.session_state.prompt_val if generate_btn is False else prompt
    
    if not active_prompt.strip():
        st.warning("⚠️ Please type a prompt or click 'Surprise Me!' to get started.")
    else:
        # Construct full prompt based on prompt and art style
        full_prompt = f"{active_prompt}, {art_style} style"
        
        # Task 3: Secretly append boost words if Magic Enhance is checked
        if magic_enhance:
            full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"
            
        # URL encode the prompt to ensure it is standard-compliant and spaces don't break the HTTP request
        encoded_prompt = urllib.parse.quote(full_prompt)
        
        # Task 1: Append width and height URL parameters properly using f-string
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"
        
        # Display feedback and image container
        with st.spinner("🎨 Creating your image... Please wait a moment."):
            try:
                import time
                response = None
                success = False
                fallback_active = False
                
                # Retry logic for robust API connection
                for attempt in range(3):
                    try:
                        response = requests.get(url, timeout=30)
                        if response.status_code == 200:
                            success = True
                            break
                        elif response.status_code == 500:
                            # Server overloaded, wait and retry
                            time.sleep(1.5)
                    except requests.exceptions.RequestException:
                        time.sleep(1.5)
                
                # Fallback logic if direct query fails (try standard default query without width/height)
                if not success:
                    fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                    try:
                        response = requests.get(fallback_url, timeout=30)
                        if response.status_code == 200:
                            success = True
                            fallback_active = True
                    except requests.exceptions.RequestException:
                        pass
                
                if success and response is not None:
                    # Render image in a premium styled container card
                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.image(response.content, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Task 2: Dynamic file name based on selected art style
                    clean_style = art_style.lower().replace(" ", "_")
                    dynamic_filename = f"{clean_style}_image.png"
                    
                    # Download Button
                    st.download_button(
                        label="📥 Download Masterpiece",
                        data=response.content,
                        file_name=dynamic_filename,
                        mime="image/png",
                        use_container_width=False
                    )
                    
                    if fallback_active:
                        st.warning("⚠️ The image was generated using default dimensions due to a temporary Pollinations AI resolution server overload.")
                    st.success("✨ Your artwork has been successfully created!")
                else:
                    status_msg = f"status code {response.status_code}" if response is not None else "no response"
                    st.error(f"❌ Error generating image: Pollinations AI API returned {status_msg}. Please try again in a few seconds or edit your prompt.")
            except requests.exceptions.RequestException as req_err:
                st.error(f"🌐 Network error: Could not reach the image generator. Detail: {req_err}")
            except Exception as e:
                st.error(f"🛑 An unexpected error occurred: {e}")
