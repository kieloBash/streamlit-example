import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import image_stitching as ist

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.subheader("Hi, I am Kielo")

# Upload multiple image files
uploaded_files = st.file_uploader("Upload two images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        # Display each uploaded image
        st.image(uploaded_file)
        
        
        
def my_function():
    st.write("Button was clicked!")

# Create a button
if st.button('Click me'):
    # Call the function when the button is clicked
    ist.stitch_image()