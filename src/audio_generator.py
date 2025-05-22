import os
from gtts import gTTS
from pydub import AudioSegment
from PIL import Image
import numpy as np

os.makedirs("generated", exist_ok=True)

def create_mp4(text, lang, tld, filename):
    temp_mp3 = os.path.join("generated", "temp.mp3")
    temp_wav = os.path.join("generated", "temp.wav")
    white_png = os.path.join("generated", "white.png")
    output_mp4 = os.path.join("generated", filename)
    tts = gTTS(text=text, lang=lang, tld=tld)
    tts.save(temp_mp3)
    audio = AudioSegment.from_mp3(temp_mp3)
    audio.export(temp_wav, format="wav")
    frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)
    img = Image.fromarray(frame.astype('uint8'))
    img.save(white_png)
    cmd = (
        f'ffmpeg -y -loop 1 -i "{white_png}" -i "{temp_wav}" '
        '-map 0:v:0 -map 1:a:0 -c:v libx264 -c:a aac '
        '-pix_fmt yuv420p -shortest -movflags +faststart -strict experimental '
        f'"{output_mp4}"'
    )
    os.system(cmd)

british_text = "Hello, I am speaking with a British accent for testing purposes."
american_text = "Hello, I am speaking with an American accent for testing purposes."
australian_text = "Hello, I am speaking with an Australian accent for testing purposes."

create_mp4(british_text, lang='en', tld='co.uk', filename="british_accent.mp4")
create_mp4(american_text, lang='en', tld='com', filename="american_accent.mp4")
create_mp4(australian_text, lang='en', tld='com.au', filename="australian_accent.mp4")

