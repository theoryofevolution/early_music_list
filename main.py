import streamlit as st
import os
import json

# Constants
KEYS_FILE = "access_keys.json"
UPLOAD_FOLDER = "uploads"

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ensure keys file exists
if not os.path.exists(KEYS_FILE):
    with open(KEYS_FILE, "w") as f:
        json.dump({}, f)

# Function to check access key
def check_access_key():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        access_key = st.text_input("🔑 Enter Access Key:", type="password")
        if st.button("Submit", key="submit_button", help="Click to submit your access key"):
            with open(KEYS_FILE, "r") as f:
                valid_keys = json.load(f)

            if access_key in valid_keys:
                del valid_keys[access_key]  # Remove key after first use
                with open(KEYS_FILE, "w") as f:
                    json.dump(valid_keys, f)
                
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Invalid or already used access key.")
        return False
    return True

def display_audio_files():
    audio_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".mp3") or f.endswith(".m4a")]
    if not audio_files:
        st.write("🎶 No music available yet.")
    else:
        for file in audio_files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            st.markdown(f"<h3 style='color: #FFD700;'>🎵 {file}</h3>", unsafe_allow_html=True)
            st.audio(file_path)

# Streamlit UI with fancy styling
st.markdown(
    """
    <style>
    body {background-color: #1e1e1e; color: white; font-family: 'Poppins', sans-serif;}
    .stApp {background-color: #1e1e1e; color: white; font-family: 'Poppins', sans-serif;}
    h1, h2, h3, h4, h5, h6 {
        color: #FFD700 !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #FFD700 !important;
        color: black !important;
        border: none !important;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:hover {
        background-color: #FFC107 !important;
    }
    .stTextInput>div>div>input {
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #FFD700 !important;
        border-radius: 6px;
        font-size: 14px;
        padding: 10px;
    }
    .stTextInput>div>div>label {
        color: #FFD700 !important;
        font-weight: bold;
    }
    .block-container {
        padding: 2rem;
        background-color: #2a2a2a;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌟 The Early Release List")

if check_access_key():
    st.subheader("🎧 Your Music Collection")
    display_audio_files()
