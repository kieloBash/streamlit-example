import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import image_stitching as ist

st.set_page_config(page_title="GRP6 DIGIMAP - IMAGE STITCHING", layout="wide", page_icon="🤖")

"""
# Welcome to ImageStitching!

Make your dream pics into one whole story! Upload images you want to make into a Panoramic Image
"""
st.subheader("CALVIN CORONADO | MICHELLE MARTINEZ | KIELO MERCADO | GHRAZIELLE RAMOS | VALEN SALIG")

# Upload multiple image files
uploaded_files = st.file_uploader("Upload two images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# Check if there are two or more uploaded images
if uploaded_files is not None and len(uploaded_files) >= 2:
    # Create a button
    if st.button('Start Stitching'):
        # Call the function when the button is clicked
        ist.stitch_images(uploaded_files)
else:
    st.warning("Please upload at least two images to start stitching.")
    
if uploaded_files is not None:
    # Display each uploaded image
    for uploaded_file in uploaded_files:
        st.image(uploaded_file)
        


