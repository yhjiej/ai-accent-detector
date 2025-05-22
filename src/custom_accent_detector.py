import numpy as np
import joblib
from tensorflow import keras
import librosa
import os
import json

with open("models/model_meta.json") as f:
    meta = json.load(f)
MAX_LEN = meta["max_len"]
N_MFCC = meta["n_mfcc"]

MODEL_PATH = os.path.join("models", "accent_model.keras")
ENCODER_PATH = os.path.join("models", "label_encoder.pkl")

model = keras.models.load_model(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

def extract_mfcc(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC)
    if mfcc.shape[1] < MAX_LEN:
        pad_width = MAX_LEN - mfcc.shape[1]
        mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :MAX_LEN]
    mfcc = mfcc.T
    return mfcc[np.newaxis, ..., np.newaxis]

def predict_accent_custom(audio_path):
    mfcc = extract_mfcc(audio_path)
    preds = model.predict(mfcc)
    idx = np.argmax(preds)
    label = label_encoder.inverse_transform([idx])[0]
    confidence = float(np.max(preds)) * 100
    explanation = f"The audio is classified as: {label} (confidence: {confidence:.1f}%)"
    return label, round(confidence, 2), explanation

