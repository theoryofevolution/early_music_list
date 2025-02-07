import streamlit as st
import os
import json

# Constants
KEYS_FILE = "access_keys.json"  # File to store allowed access keys
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
        access_key = st.text_input("Enter Access Key:", type="password")
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
                st.error("Invalid or already used access key. Contact Yash for access.")
        return False
    return True

# Function to display audio files
def display_audio_files():
    audio_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".mp3") or f.endswith(".m4a")]
    if not audio_files:
        st.write("No music available yet.")
    else:
        for file in audio_files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            st.markdown(
                f"""
                <div style="
                    background-color: #FFD700;
                    padding: 15px;
                    border-radius: 12px;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
                    text-align: center;
                    margin-bottom: 10px;
                    font-family: 'Poppins', sans-serif;
                ">
                    <h3 style="color: black;">🎵 {file}</h3>
                    <audio controls style="width: 100%;" controlsList="nodownload">
                        <source src="{UPLOAD_FOLDER}/{file}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Streamlit UI
st.markdown(
    """
    <style>
    body {background-color: white; color: black; font-family: 'Poppins', sans-serif;}
    .stApp {background-color: white; color: black; font-family: 'Poppins', sans-serif;}
    h1, h2, h3, .stTitle, .stHeader, .stSubheader {
        color: black !important;
        font-weight: bold;
        font-family: 'Poppins', sans-serif;
    }
    label {color: black !important; font-weight: bold; font-family: 'Poppins', sans-serif;}
    .stMarkdown {color: black !important; font-family: 'Poppins', sans-serif;}
    .stApp>header {display: none !important;}
    .stButton>button {
        background-color: gold !important;
        color: black !important;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Yash's Early Release List")

if check_access_key():
    st.subheader("Your Music")
    display_audio_files()
