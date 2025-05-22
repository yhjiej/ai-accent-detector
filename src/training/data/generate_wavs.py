from gtts import gTTS
from pydub import AudioSegment
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

texts = {
    "american": [
        "Hello, how are you doing today? This is an example of American English.",
        "Can you please help me with this problem?",
        "It's a beautiful day outside.",
        "I'm looking forward to the weekend.",
        "Let's grab a cup of coffee together."
    ],
    "british": [
        "Good morning, how are you today? This is a British accent demonstration.",
        "Could you assist me with this matter, please?",
        "The weather is lovely, isn't it?",
        "I'm excited for the holiday.",
        "Shall we have a cup of tea?"
    ],
    "australian": [
        "G'day mate, how's it going? This is an Australian English accent.",
        "Can you give me a hand with this?",
        "It's a sunny day here in Australia.",
        "Looking forward to the footy this weekend.",
        "Let's have a barbecue together."
    ]
}

NB_FILES = 5

tld_map = {
    "american": "com",
    "british": "co.uk",
    "australian": "com.au"
}

for accent in texts:
    accent_dir = os.path.join(BASE_DIR, accent)
    os.makedirs(accent_dir, exist_ok=True)
    for i in range(NB_FILES):
        text = texts[accent][i % len(texts[accent])]
        tts = gTTS(text=text, lang='en', tld=tld_map[accent])
        mp3_path = os.path.join(accent_dir, f"{accent}_{i:03d}.mp3")
        wav_path = os.path.join(accent_dir, f"{accent}_{i:03d}.wav")
        tts.save(mp3_path)
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")
        os.remove(mp3_path)
        print(f"✔️ {wav_path} generated")

print("✅ All wav files generated successfully.")
