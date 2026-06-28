import streamlit as st
import requests

# 1. Page Title and Layout Setup
st.set_page_config(page_title="Arch-Eco Spatial Planner", layout="centered")

# --- CUSTOM EXPERT BRAND COLORS ---
# This changes the app background to a welcoming, professional, ultra-soft green tint (#f0f4f1)
# and styles the main containers with your new premium sage/forest palette.
# --- CUSTOM EXPERT BRAND COLORS ---
# --- CUSTOM EXPERT BRAND COLORS ---
st.markdown(
    """
    <style>
    /* 1. App Background */
    .stApp {
        background-color: #fcfbfa; /* Premium Linen White background */
    }
    
    /* 2. Main Typography Colors */
    h1 {
        color: #1e3e2b !important; /* Deep Forest Green */
    }
    h3 {
        color: #5a8266 !important; /* Muted Sage Green */
    }
    .stApp p, .stApp label {
        color: #1e3e2b !important; /* Deep Forest Green for labels */
    }
    
    /* 3. FIX: Dropdown Input & File Uploader Text Color to White */
    /* This makes the selected city name and uploader details readable against dark inputs */
    .stSelectbox div[data-baseweb="select"] div {
        color: white !important;
    }
    .stFileUploader section div {
        color: white !important;
    }
    .stFileUploader small {
        color: #cccccc !important; /* Soft light gray for the "200MB per file" subtext */
    }
    
    /* 4. Action Button Styling */
    div.stButton > button:first-child {
        background-color: #1e3e2b;
        color: white !important;
        border-radius: 6px;
        border: none;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #5a8266;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- MAIN INTERFACE DISPLAY ---
st.title("🏛️ Arch-Eco Contextual Spatial Planner")
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
        N8N_WEBHOOK_URL = "https://eshalnajam.app.n8n.cloud/webhook-test/archeco-receiver"
        
        # Package the data to send to n8n
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        data = {"city": city}
        
        try:
            # Send payload to n8n
            response = requests.post(N8N_WEBHOOK_URL, files=files, data=data)
            
            if response.status_code == 200:
                st.success("Analysis Complete!")
                
                # Display report
                report_text = response.text
                st.markdown(report_text)
                
                st.write("---") 
                
                # Download Button for the file output
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
