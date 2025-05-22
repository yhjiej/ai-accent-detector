# English Accent Detection Tool 🇬🇧🇺🇸🇦🇺

A complete pipeline to **generate English accent training data, train your own accent classification model, and use a Streamlit app to detect language or accent** from video or audio.

---

## 🧩 Features

* **Data Generation:** Easily generate labeled audio files (American, British, Australian accents) with TTS for fast dataset creation.
* **Model Training:** Train a custom neural network on your own or generated data to classify between American, British, and Australian accents.
* **Detection App:**

  * Detects if the speaker is speaking English (using SpeechBrain)
  * Classifies English accents (American/British/Australian) with your trained model
  * Works from **public video URLs (MP4, Loom, etc.)** or **uploaded files**

---

## 🚀 How to Use

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate synthetic training data (optional)

You can generate x audio samples per accent using:

```bash
python src/training/generate_wavs.py
```

This will create `.wav` files in `src/training/data/american/`, `british/`, `australian/`.

### 3. Train your custom accent model

Train on the generated data (or your own real data):

```bash
python src/training/train.py
```

This saves the trained model, encoder, and meta info into `models/`.

### 4. Launch the Streamlit detection app

```bash
streamlit run app.py
```

### 5. Use the app

* Paste a public video URL **or** upload a video file.
* Choose: “Language detection (SpeechBrain)” or “Accent detection (custom Keras model)”
* The app extracts audio, runs the chosen detection, and displays the result.

---

## 🛠 Tech Stack

* **Python**
* **Streamlit**
* **MoviePy**
* **SpeechBrain** (language detection)
* **TensorFlow / Keras** (accent classification)
* **librosa, gTTS, pydub** (audio feature extraction & TTS)
* **scikit-learn** (label encoding)

---

## 📝 Limitations

* Accent classification is only as good as the diversity/quality of your training data.
* Models trained on synthetic voices may not generalize perfectly to real-world accents.
* For production use, expand the dataset with more diverse, real speech.

---

## 📂 Project Structure

```
accent-detector/
│
├── src/
│   ├── audio_utils.py
│   ├── accent_detector.py            # SpeechBrain (language detection)
│   ├── custom_accent_detector.py     # Custom accent classification
│   └── training/
│        ├── generate_wavs.py         # Data generation
│        ├── train.py                 # Model training
│        └── ... (utilities, etc.)
├── models/                           # Trained model, label encoder, and metadata
├── data/                             # Uploaded/extracted files for the app
├── app.py                            # Streamlit web app
├── requirements.txt
└── README.md
```

---

This project demonstrates:

* **Full ML pipeline skills:** from dataset creation, feature extraction, and model training to deployment and inference
* **Modern Python engineering:** reusable modules, clear project organization, and clean separation of training/inference logic
* **User-focused deployment:** a real, interactive app ready to test with any video

---