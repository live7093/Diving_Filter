import streamlit as st
import numpy as np
from PIL import Image
import requests

st.set_page_config(layout="centered")  # keeps the layout tight

# --- Enhancement function ---
def enhance_red_areas(img_rgb, strength=1.5, red_threshold=0.2):
    img_float = img_rgb.astype(np.float32) / 255.0
    red_channel = img_float[:, :, 0]
    green_channel = img_float[:, :, 1]
    blue_channel = img_float[:, :, 2]

    red_mask = (red_channel > red_threshold) & (red_channel > green_channel) & (red_channel > blue_channel)
    enhanced = img_float.copy()
    enhanced[:, :, 0][red_mask] *= strength
    enhanced = np.clip(enhanced, 0, 1)
    return (enhanced * 255).astype(np.uint8)

# --- UI ---
st.markdown("""
    <div style='text-align: center; max-width: 800px; margin: auto;'>
        <h1>🤿 Underwater Red Correction Tool</h1>
        <p>Upload your underwater photo, then choose the approximate depth.  
        The app will intelligently enhance red tones lost due to underwater color absorption.</p>
    </div>
""", unsafe_allow_html=True)

# Upload image
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
else:
    st.info("No image uploaded. Using a sample image.")
    image = Image.open(requests.get(
        "https://i.kym-cdn.com/entries/icons/facebook/000/022/747/Do_Something_meme_banner_imag.jpg", 
        stream=True).raw).convert("RGB")

# Select depth → tune red enhancement
depth_choice = st.selectbox("🌊 Approximate Depth (meters)", [5, 10, 15])
depth_to_strength = {5: 1.3, 10: 1.6, 15: 1.9}
enhancement_strength = depth_to_strength[depth_choice]

# Enhance image
img_rgb = np.array(image)
enhanced_img = enhance_red_areas(img_rgb, strength=enhancement_strength, red_threshold=0.15)

# Display both images
tab1, tab2 = st.tabs(["🎨 Color Corrected", "📷 Original"])
tab1.image(enhanced_img, use_container_width=True, caption="Red-enhanced image")
tab2.image(img_rgb, use_container_width=True, caption="Original image")
