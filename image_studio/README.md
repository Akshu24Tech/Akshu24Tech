# Upgraded AI Image Studio 🎨

An interactive, high-performance web application built with Streamlit that interfaces with the Pollinations AI Image Generation API. This project was built and upgraded as part of the **MirAI School of Technology Virtual Summer Internship 2026** ("AI Builder" Track).

## 🚀 Features & Upgrades

### 1. Fully Functional Resolution Sliders (Task 1)
- **The Bug:** Previously, the width and height sliders in the UI did not affect the output image size because they weren't appended to the request URL.
- **The Fix:** Integrated width and height dimensions as HTTP query parameters (`?width=...&height=...`) into the final Pollinations URL.

### 2. Dynamic PNG Downloads (Task 2)
- **The Bug:** The downloaded image file lacked a file extension, leaving operating systems unable to open it directly.
- **The Fix:** Formatted download buttons to append `.png` correctly.
- **Bonus:** Made download file names dynamic based on the chosen art style (e.g. `anime_image.png`, `cinematic_image.png`).

### 3. "Magic Enhance" Smart Prompt Booster (Task 3)
- Enabled a sidebar checkbox to inject high-quality descriptor tokens (`masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render`) behind-the-scenes to boost simple user prompts.

### 4. "Surprise Me!" Creative Prompts (Task 4)
- Added a dedicated button that utilizes standard Python random selection to pick from a curated list of creative prompts and immediately generate an image.

---

## 🛠️ How to Run Locally

1. **Navigate to the workspace folder:**
   ```bash
   cd C:\Users\techl\mirai\image_studio
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

4. Open the local address in your browser: `http://localhost:8501`
