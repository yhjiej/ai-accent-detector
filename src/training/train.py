from src.train_model import build_and_train_model
import joblib
import os
import json

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

print("📊 Training the model...")
model, encoder, max_len, n_mfcc = build_and_train_model()

model.save(os.path.join(MODEL_DIR, "accent_model.keras"))
joblib.dump(encoder, os.path.join(MODEL_DIR, "label_encoder.pkl"))

meta = {"max_len": max_len, "n_mfcc": n_mfcc}
with open(os.path.join(MODEL_DIR, "model_meta.json"), "w") as f:
    json.dump(meta, f)
print(f"✅ Model and metadata successfully saved in {MODEL_DIR}/")
