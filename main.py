import streamlit as st
import os
import json

# Constants
UPLOAD_FOLDER = "uploads"
ACCESS_KEY_FILE = "access_keys.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load access keys from the JSON file
def load_access_keys():
    with open(ACCESS_KEY_FILE, "r") as file:
        return json.load(file)

# Save updated access keys to the JSON file
def save_access_keys(access_keys):
    with open(ACCESS_KEY_FILE, "w") as file:
        json.dump(access_keys, file, indent=4)

# Function to display the audio files
def display_audio_files():
    st.markdown("<h2 style='text-align: center;'>l'avant-première</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)
    
    audio_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".mp3", ".m4a"))]
    if not audio_files:
        st.write("🎶 No music available yet.")
    else:
        for file in audio_files:
            abs_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, file))
            st.markdown(f"**{file}**")
            st.audio(abs_path)
            st.markdown("<hr style='border: 0.5px solid #ddd;'>", unsafe_allow_html=True)

# Function to handle the access key submission
# Function to handle access key submission
def handle_access_key_submission():
    access_keys = load_access_keys()
    access_key = st.text_input("", type="password", placeholder="Access Key", key="access_input")
    submit_col = st.columns([3, 1, 3])[1]

    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    with submit_col:
        if st.button("Submit"):
            st.session_state["submitted"] = True
            if access_key in access_keys:
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = access_keys[access_key]
                del access_keys[access_key]
                save_access_keys(access_keys)
                st.rerun()
            else:
                st.session_state["invalid_key"] = True

    if st.session_state.get("submitted") and st.session_state.get("invalid_key"):
        st.error("❌ Invalid or already used access key.")

# Main section
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    st.markdown(f"<h2 style='text-align: center;'>Welcome, {st.session_state['user_name']}!</h2>", unsafe_allow_html=True)
    display_audio_files()
else:
    st.markdown("<h2 style='text-align: center;'>🔑 Enter Access Key</h2>", unsafe_allow_html=True)
    handle_access_key_submission()
