import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests

# Streamlit UI
st.markdown("""
    <h1 style='text-align: center;'>🤿 Underwater Red Correction Tool</h1>
    <p style='text-align: center;'>Welcome to the Underwater Red Color Image Processor!  
Upload your underwater photo below, then choose the approximate depth it was taken at.  
The app will enhance the red channel to correct underwater color loss.</p>
""", unsafe_allow_html=True)


# Upload image
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
else:
    st.info("No image uploaded. Using a sample meme image instead.")
    image = Image.open(requests.get(
        "https://i.kym-cdn.com/entries/icons/facebook/000/022/747/Do_Something_meme_banner_imag.jpg", 
        stream=True).raw).convert("RGB")

# Depth selection
depth_choice = st.selectbox("🌊 Select Approximate Depth (in meters)", [5, 10, 15])

# Depth-based red filter strength
depth_to_strength = {
    5: 0.10,
    10: 0.20,
    15: 0.30
}
red_strength = depth_to_strength[depth_choice]

# Convert image for processing
img_rgb = np.array(image)
img_float = img_rgb.astype(np.float32) / 255.0

# Create red filter overlay
red_mask = np.zeros_like(img_float)
red_mask[:, :, 0] = 1.0  # Red channel full

# Blend image with red mask
filtered_img = img_float * (1 - red_strength) + red_mask * red_strength
filtered_img = np.clip(filtered_img, 0, 1)
filtered_img_uint8 = (filtered_img * 255).astype(np.uint8)

# Display results in tabs
tab1, tab2 = st.tabs(["🎨 Color Corrected", "📷 Original"])
tab1.image(filtered_img_uint8, use_container_width=True, caption="Red-enhanced image")
tab2.image(img_rgb, use_container_width=True, caption="Original image")
