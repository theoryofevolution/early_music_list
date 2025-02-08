import streamlit as st
import os
import json

# Constants
UPLOAD_FOLDER = "uploads"
ACCESS_KEY_FILE = "access_keys.json"
MASTER_PASSWORD = "supersecretpassword"  # Change this to your desired master password
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load access keys from the JSON file
def load_access_keys():
    if not os.path.exists(ACCESS_KEY_FILE):
        with open(ACCESS_KEY_FILE, "w") as file:
            json.dump({}, file)  # Create an empty JSON file if it doesn't exist
    with open(ACCESS_KEY_FILE, "r") as file:
        return json.load(file)

# Save updated access keys to the JSON file
def save_access_keys(access_keys):
    with open(ACCESS_KEY_FILE, "w") as file:
        json.dump(access_keys, file, indent=4)

# Function to display only the most recent audio file
def display_latest_audio_file():
    st.markdown("<h2 style='text-align: center;'>l'avant-première</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #ccc; margin: 20px 0;'>", unsafe_allow_html=True)
    
    audio_files = sorted([f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".mp3", ".m4a"))], reverse=True)
    if not audio_files:
        st.write("🎶 No music available yet.")
    else:
        latest_file = audio_files[0]
        abs_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, latest_file))
        st.markdown(f"**{latest_file}**")
        st.audio(abs_path)

# Master user dashboard for managing access keys and uploading/deleting music
def master_user_dashboard():
    st.markdown("<h2 style='text-align: center;'>Master User Dashboard</h2>", unsafe_allow_html=True)
    
    # Access key management
    st.markdown("### Manage Access Keys")
    access_keys = load_access_keys()
    
    # Display existing keys
    if access_keys:
        st.markdown("**Existing Access Keys:**")
        for key, name in access_keys.items():
            st.write(f"**{key}** → {name}")
    else:
        st.write("No access keys available.")
    
    # Form to add a new access key
    st.markdown("### Add a New Access Key")
    new_user_name = st.text_input("User Name")
    new_access_key = st.text_input("Access Key")
    
    if st.button("Add Access Key"):
        if new_user_name and new_access_key:
            access_keys[new_access_key] = new_user_name
            save_access_keys(access_keys)
            st.success(f"Access key for {new_user_name} added successfully!")
            st.rerun()
        else:
            st.error("Please fill in both the user name and access key.")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Music upload section
    st.markdown("### Upload New Music")
    uploaded_file = st.file_uploader("Choose a music file (.mp3 or .m4a)", type=["mp3", "m4a"])
    
    if uploaded_file:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"{uploaded_file.name} uploaded successfully!")
        st.rerun()

    # Music management section
    st.markdown("### Manage Uploaded Music")
    audio_files = sorted([f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".mp3", ".m4a"))], reverse=True)
    
    if not audio_files:
        st.write("No music uploaded yet.")
    else:
        for file in audio_files:
            col1, col2 = st.columns([8, 2])
            col1.write(f"**{file}**")
            if col2.button("❌ Remove", key=f"remove_{file}"):
                file_path = os.path.join(UPLOAD_FOLDER, file)
                os.remove(file_path)
                st.success(f"{file} has been removed.")
                st.rerun()

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
            if access_key in access_keys or access_key == MASTER_PASSWORD:
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = access_keys.get(access_key, "Master User")
                
                # Remove the access key from the file if it’s not the master password
                if access_key != MASTER_PASSWORD and access_key in access_keys:
                    del access_keys[access_key]
                    save_access_keys(access_keys)
                
                st.rerun()
            else:
                st.session_state["invalid_key"] = True

    if st.session_state.get("submitted") and st.session_state.get("invalid_key"):
        st.error("❌ Invalid or already used access key.")

# Main section
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    if st.session_state["user_name"] == "Master User":
        master_user_dashboard()
    else:
        st.markdown(f"<h2 style='text-align: center;'>Welcome, {st.session_state['user_name']}!</h2>", unsafe_allow_html=True)
        display_latest_audio_file()
else:
    st.markdown("<h2 style='text-align: center;'>🔑 Enter Access Key</h2>", unsafe_allow_html=True)
    handle_access_key_submission()
