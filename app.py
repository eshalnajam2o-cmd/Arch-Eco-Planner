import streamlit as st
import requests

# 1. Page Title and Layout Setup
st.set_page_config(page_title="Arch-Eco Spatial Planner", layout="centered")

# --- LOGO THEME BACKGROUND & TYPOGRAPHY STYLE ---
st.markdown(
    """
    <style>
    /* 1. App Background - Smooth gradient using your exact logo brand colors */
    .stApp {
        background: linear-gradient(135deg, #1e3e2b 0%, #30543d 50%, #5a8266 100%);
        background-attachment: fixed;
    }
    
    /* 2. Main Typography Colors - Set to highly readable contrasting light tones */
    h1 {
        color: #fcfbfa !important; /* Premium Linen White */
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    h3 {
        color: #cbdad0 !important; /* Extremely Soft Mint/Sage Gray */
        margin-top: 5px !important;
    }
    .stApp p, .stApp label {
        color: #fcfbfa !important; /* Linen White for clear paragraph text */
    }
    
    /* 3. Input Elements Visibility Controls */
    /* Selectbox Styling */
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 6px;
    }
    .stSelectbox div[data-baseweb="select"] div {
        color: white !important;
    }
    
    /* File Uploader Container Styling */
    .stFileUploader section {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px;
    }
    .stFileUploader section div {
        color: white !important;
    }
    .stFileUploader button, 
    .stFileUploader button p, 
    .stFileUploader button span {
        color: #1e3e2b !important; /* Make the small browse button dark green for crisp readability */
        background-color: white !important;
        border-radius: 4px;
    }
    .stFileUploader small {
        color: #cbdad0 !important; 
    }
    
    /* 4. Action Button Styling (Optimize My Design Button) */
    div.stButton > button:first-child {
        background-color: #fcfbfa !important; /* Bright white button to pop off the green gradient */
        border-radius: 6px;
        border: none;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    div.stButton > button:first-child *,
    div.stButton > button:first-child p,
    div.stButton > button:first-child span {
        color: #1e3e2b !important; /* Dark text inside the white button */
    }
    div.stButton > button:first-child:hover {
        background-color: #cbdad0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIDE-BY-SIDE HEADER LAYOUT (Matching Your Sketch) ---
# Create two horizontal columns: Column 1 for the Logo, Column 2 for the Header texts
col1, col2 = st.columns([1, 3.5], vertical_alignment="center")

with col1:
    # Safely load your premium circular icon without asset path errors
    LOGO_URL = logo.jpeg
    st.image(LOGO_URL, use_container_width=True)

with col2:
    st.title("Arch-Eco Contextual Spatial Planner")

# Description paragraph flows elegantly right below the header row
st.write("Upload your 2D sketch and select your city to optimize your design for local climate constraints.")
st.write("---")

# --- USER INPUT CONTROLS ---
city = st.selectbox(
    "Select the project location (Climate Zone):",
    ["Islamabad (Humid Subtropical / Hot)", "Lahore (Semi-Arid / Intense Heat)", "Karachi (Arid / Coastal Humid)"]
)

uploaded_file = st.file_uploader("Upload your hand-drawn 2D layout (PNG or JPG)", type=["png", "jpg", "jpeg"])

st.write("") # Spacer

# --- TRIGGER EXECUTION ---
if st.button("Optimize My Design"):
    if uploaded_file is not None:
        st.info("Processing your design with human design DNA and AI analysis...")
        
        N8N_WEBHOOK_URL = "https://eshalnajam.app.n8n.cloud/webhook-test/archeco-receiver"
        
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        data = {"city": city}
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, files=files, data=data)
            
            if response.status_code == 200:
                st.success("Analysis Complete!")
                report_text = response.text
                st.markdown(report_text)
                
                st.write("---") 
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
