import streamlit as st
import requests
import urllib.parse

BACKEND_URL = "http://backend:8000"  # or http://localhost:8000 during local testing

st.set_page_config(page_title="📁 AWS Drive", layout="centered")

st.sidebar.info("🚀 Uses FastAPI, Streamlit, AWS S3 & SQLite")

st.title("📁 Google Drive Clone")

# Upload
st.subheader("📤 Upload a File")
with st.form("upload_form"):
    uploaded_file = st.file_uploader("Choose a file to upload")
    submit = st.form_submit_button("Upload")

    if submit and uploaded_file:
        files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
        res = requests.post(f"{BACKEND_URL}/upload", files=files)
        if res.status_code == 200:
            st.success(f"{uploaded_file.name} uploaded ✅")
            st.rerun()
        else:
            st.error(res.json().get("detail"))

# View Files
st.subheader("📂 Stored Files")

res = requests.get(f"{BACKEND_URL}/view")
if res.status_code == 200:
    files = res.json()
    if not files:
        st.info("No files uploaded yet.")
    for filename in files:
        col1, col2, col3 = st.columns([5, 1, 1])
        col1.write(f"📄 {filename}")

        # Download
        with col2:
            dl = requests.get(f"{BACKEND_URL}/download/{urllib.parse.quote(filename)}")
            if dl.status_code == 200:
                st.markdown(f"[⬇️ ]({dl.json()['url']})", unsafe_allow_html=True)

        # Delete
        if col3.button("❌", key=filename):
            del_res = requests.delete(f"{BACKEND_URL}/delete/{urllib.parse.quote(filename)}")
            if del_res.status_code == 200:
                st.success(f"{filename} deleted!")
                st.rerun()
else:
    st.error("Error fetching files.")
