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
        if st.button("Submit", key="submit_button"):
            with open(KEYS_FILE, "r") as f:
                valid_keys = json.load(f)
            if access_key in valid_keys:
                del valid_keys[access_key]
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
        st.write("<div style='text-align: center;'>🎶 No music available yet.</div>", unsafe_allow_html=True)
    else:
        for file in audio_files:
            file_path = os.path.join(UPLOAD_FOLDER, file)
            st.markdown(f"<h3 style='color: #FFD700; text-align: center;'>🎵 {file}</h3>", unsafe_allow_html=True)
            st.audio(file_path)

# Streamlit UI with fancy centered styling
st.markdown(
    """
    <style>
    body {background-color: #1e1e1e; color: white; font-family: 'Poppins', sans-serif;}
    .stApp {background-color: #1e1e1e; color: white; font-family: 'Poppins', sans-serif;}
    h1, h2, h3, h4, h5, h6 {
        color: #FFD700 !important;
        font-weight: bold;
        text-align: center;
    }
    .block-container {
        padding: 2rem;
        background-color: #2a2a2a;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        max-width: 800px;
        margin: auto;
    }
    header {display: none !important;}
    .stToolbar {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Injecting JavaScript to hide the top bar
st.components.v1.html(
    """
    <script>
        const interval = setInterval(() => {
            const topBar = window.parent.document.querySelector('header');
            if (topBar) {
                topBar.style.display = 'none';
                clearInterval(interval);
            }
        }, 100);
    </script>
    """,
    height=0,
)

# Centered title and subheader
st.title("The Early Release List")

if check_access_key():
    st.subheader("🎧 Your Music Collection")
    display_audio_files()
