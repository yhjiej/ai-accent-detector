import os
import requests
import subprocess

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    from moviepy.video.io.VideoFileClip import VideoFileClip

def download_video(url, filename="data/uploaded/video.mp4"):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def extract_audio(video_path, audio_path):
    tmp_wav = os.path.join(os.path.dirname(audio_path), "tmp_audio.wav")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(tmp_wav)
    subprocess.run([
        "ffmpeg", "-y", "-i", tmp_wav,
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        audio_path
    ], check=True)
    try:
        os.remove(tmp_wav)
    except Exception:
        pass