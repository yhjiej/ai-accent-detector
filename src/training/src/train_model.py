import os
import numpy as np
from src.extract_features import extract_mfcc
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models

def load_dataset(base_dir="src/training/data"):
    X, y = [], []
    for label in os.listdir(base_dir):
        path = os.path.join(base_dir, label)
        if not os.path.isdir(path): continue

        for file in os.listdir(path):
            if file.endswith(".wav"):
                mfcc = extract_mfcc(os.path.join(path, file))
                X.append(mfcc)
                y.append(label)

    if not X:
        raise ValueError("No audio file found!")

    max_len = max([mfcc.shape[0] for mfcc in X])
    n_mfcc = X[0].shape[1]

    X = [np.pad(mfcc, ((0, max_len - mfcc.shape[0]), (0, 0)), mode='constant') for mfcc in X]
    X = np.array(X)[..., np.newaxis]

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    y = le.fit_transform(y)
    from sklearn.model_selection import train_test_split
    return train_test_split(X, y, test_size=0.2), le, max_len, n_mfcc


def build_and_train_model():
    (X_train, X_test, y_train, y_test), le, max_len, n_mfcc = load_dataset()

    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=X_train.shape[1:]),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(len(le.classes_), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
    return model, le, max_len, n_mfcc
