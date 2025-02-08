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
        if st.button("Submit"):
            with open(KEYS_FILE, "r") as f:
                valid_keys = json.load(f)
            
            if access_key in valid_keys:
                del valid_keys[access_key]  # Remove key after first use
                with open(KEYS_FILE, "w") as f:
                    json.dump(valid_keys, f)
                
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Invalid or already used access key.")
        return False
    return True

def display_audio_files():
    audio_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".mp3") or f.endswith(".m4a")]
    if not audio_files:
        st.write("No music available yet.")
    else:
        for file in audio_files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            st.write(f"### 🎵 {file}")
            st.audio(file_path)

# Streamlit UI
st.title("The Early Release List")

if check_access_key():
    st.subheader("Your Music")
    display_audio_files()
