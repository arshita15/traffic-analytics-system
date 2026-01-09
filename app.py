import streamlit as st
import os
import shutil
import subprocess

st.set_page_config(page_title="Traffic Analytics System", layout="centered")

st.title("🚦 Traffic Analytics System")
st.write("Upload a traffic video to run vehicle detection, tracking, direction, and speed analysis.")

UPLOAD_DIR = "data/input"
OUTPUT_DIR = "output"
VIDEO_PATH = os.path.join(UPLOAD_DIR, "video.mp4")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

uploaded_file = st.file_uploader("Upload input video", type=["mp4"])

if uploaded_file is not None:
    with open(VIDEO_PATH, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video uploaded successfully.")

    if st.button("Run Traffic Analysis"):
        st.info("Processing video. This may take a few minutes...")

        try:
            subprocess.run(
                ["python", "-m", "src.pipeline"],
                check=True
            )
            st.success("Processing completed successfully!")

            st.write("### Outputs generated:")
            st.write("- Annotated video: `output/annotated_video.mp4`")
            st.write("- Results CSV: `output/results.csv`")
            st.write("- Speed summary CSV: `output/speed_summary.csv`")

        except subprocess.CalledProcessError:
            st.error("Error occurred while running the pipeline.")
