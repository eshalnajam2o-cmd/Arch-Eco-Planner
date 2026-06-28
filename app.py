import streamlit as st
import requests
# 1. Page Title and Layout Setup
st.set_page_config(page_title="Arch-Eco Spatial Planner", layout="centered")

# --- CUSTOM BACKGROUND & THEME COLOR ---
# This changes the app background to a clean, soft architectural slate/light gray tone
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f6f7;
    }
    </style>
    """,
    unsafe_allow_index=True,
    unsafe_allow_html=True
)

# --- TOP LEFT LOGO POSITIONING ---
# Moving the new circular logo icon directly into the top left sidebar space
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.write("---")
    st.caption("📍 Core System Active")
# 1. Page Title and Styling
st.set_page_config(page_title="Arch-Eco Spatial Planner", layout="centered")
st.title(" Arch-Eco Contextual Spatial Planner")
st.write("Upload your 2D sketch and select your city to optimize your design for local climate constraints.")

# 2. User Inputs
city = st.selectbox(
    "Select the project location (Climate Zone):",
    ["Islamabad (Humid Subtropical / Hot)", "Lahore (Semi-Arid / Intense Heat)", "Karachi (Arid / Coastal Humid)"]
)

uploaded_file = st.file_uploader("Upload your hand-drawn 2D layout (PNG or JPG)", type=["png", "jpg", "jpeg"])

# 3. Trigger Button
if st.button("Optimize My Design"):
    if uploaded_file is not None:
        st.info("Processing your design with human design DNA and AI analysis...")
        
        # --- CONNECTING TO N8N ---
        # Replace the URL below with your actual n8n webhook URL
        N8N_WEBHOOK_URL = "https://eshalnajam.app.n8n.cloud/webhook-test/archeco-receiver"
        
        # Package the data to send to n8n
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        data = {"city": city}
        
        try:
            # This line physically sends the image and city over the internet to n8n
            response = requests.post(N8N_WEBHOOK_URL, files=files, data=data)
            
            if response.status_code == 200:
                st.success("Analysis Complete!")
                
                # 1. Display the report on the screen
                report_text = response.text
                st.markdown(report_text)
                
                st.write("---") # Visual divider line
                
                # 2. Add a clean Download Button for your users
                st.download_button(
                    label="📥 Download Architecture Report (.txt)",
                    data=report_text,
                    file_name="arch_eco_optimization_report.txt",
                    mime="text/plain"
                )
            else:
                st.error("Error communicating with the AI workflow engine.")
        except Exception as e:
            st.error(f"Could not connect to n8n: {e}")
            
    else:
        st.warning("Please upload a sketch first!")
