import streamlit as st
import requests
from PIL import Image
import io

# Replace with your actual n8n production or test webhook URL
N8N_WEBHOOK_URL = "https://your-n8n-instance.hooks.n8n.cloud/xxxx-xxxx-xxxx"

st.set_page_config(page_title="Arch-Eco Contextual Spatial Planner", layout="wide")

st.title("🏛️ Arch-Eco Contextual Spatial Planner")
st.write("Upload a hand-drawn sketch to generate a culturally relevant, energy-efficient spatial plan.")

# Sidebar for inputs
st.sidebar.header("Context Parameters")
location = st.sidebar.selectbox("Select Regional Climate Zone:", ["Islamabad (Hot Summer/Mild Winter)", "Lahore (Semi-Arid/Intense Heat)", "Karachi (Humid/Coastal)"])
design_style = st.sidebar.selectbox("Design DNA:", ["Biophilic South Asian Courtyard", "Modern Minimalist with Local Materials"])

# File Uploader
uploaded_file = st.file_uploader("Upload 2D Floor Plan Sketch (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Layout Sketch", use_container_width=True)
    
    if st.button("Analyze & Optimize Layout"):
        with st.spinner("Analyzing layout against environmental matrix..."):
            try:
                # Convert image to bytes for sending
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format)
                img_byte_arr = img_byte_arr.getvalue()
                
                # Prepare data and files for n8n
                files = {"file": (uploaded_file.name, img_byte_arr, uploaded_file.type)}
                data = {"location": location, "style": design_style}
                
                # Send to n8n
                response = requests.post(N8N_WEBHOOK_URL, data=data, files=files)
                
                if response.status_code == 200:
                    st.success("Analysis Complete!")
                    st.markdown(response.text) # Renders the AI's structural markdown report
                else:
                    st.error(f"Error from server: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
