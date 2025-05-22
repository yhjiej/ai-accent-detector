import streamlit as st
from src.audio_utils import download_video, extract_audio
from src.accent_detector import predict_accent
from src.custom_accent_detector import predict_accent_custom
import os

UPLOAD_DIR = "data/uploaded"
AUDIO_DIR = "data/audio_generated"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

st.title("English Accent Detection Tool 🇬🇧🇺🇸🇦🇺")
st.write("Upload a video file (MP4), or enter a public video URL (MP4, Loom, etc.)")

tab1, tab2 = st.tabs(["By URL", "By Upload"])
video_path = None

with tab1:
    url = st.text_input("Enter a public video URL")
    if st.button("Analyze (from URL)"):
        try:
            st.info("Downloading video...")
            video_path = os.path.join(UPLOAD_DIR, "video.mp4")
            download_video(url, video_path)
            st.success(f"Video downloaded as {video_path}.")
        except Exception as e:
            st.error(f"Error downloading video: {str(e)}")

with tab2:
    uploaded_file = st.file_uploader("Upload your video file (MP4 only)", type=["mp4"])
    if uploaded_file is not None:
        video_path = os.path.join(UPLOAD_DIR, "uploaded_video.mp4")
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded as {video_path}.")

st.markdown("### Choose detection mode")
analysis_mode = st.selectbox(
    "Detection mode",
    ["Language detection (SpeechBrain)", "Accent detection (custom Keras model)"]
)

if video_path and st.button("Extract Audio & Analyze", key="analyze_btn"):
    try:
        audio_path = os.path.join(AUDIO_DIR, "audio.wav")
        st.info("Extracting audio...")
        extract_audio(video_path, audio_path)
        st.success(f"Audio extracted as {audio_path}.")

        st.info("Analyzing...")
        if analysis_mode == "Language detection (SpeechBrain)":
            label, confidence, explanation = predict_accent(audio_path)
            if isinstance(label, list):
                label = label[0]
            if label.lower() == "english":
                st.success(f"English language detected! Confidence: {confidence}%")
            else:
                st.warning(f"Detected language: {label}. (Confidence: {confidence}%)")
        else:
            label, confidence, explanation = predict_accent_custom(audio_path)
            st.success(f"Detected accent: {label} (Confidence: {confidence}%)")

        st.markdown(f"**Summary:** {explanation}")

        # Nettoyage du fichier uploadé si besoin
        if os.path.basename(video_path) == "uploaded_video.mp4":
            try:
                os.remove(video_path)
            except Exception:
                pass

    except Exception as e:
        st.error(f"Error: {str(e)}")
