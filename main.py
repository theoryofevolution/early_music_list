import streamlit as st
import os

# Constants
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload folder exists

# Function to check access key using st.secrets
def check_access_key():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        access_key = st.text_input("🔑 Enter Access Key:", type="password")
        if st.button("Submit"):
            if access_key == st.secrets["ACCESS_KEY"]:  # Use Streamlit's secrets for secure access keys
                st.session_state["authenticated"] = True
                st.success("Access granted.")
                st.rerun()
            else:
                st.error("❌ Invalid access key.")
        return False
    return True

# Function to display audio files
def display_audio_files():
    audio_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".mp3", ".m4a"))]
    if not audio_files:
        st.write("🎶 No music available yet.")
    else:
        for file in audio_files:
            st.markdown(f"<h3 style='text-align: center;'>🎵 {file}</h3>", unsafe_allow_html=True)
            st.audio(os.path.join(UPLOAD_FOLDER, file))

# Streamlit UI with minimal styling
st.title("The Early Release List")
if check_access_key():
    st.subheader("Music")
    display_audio_files()
