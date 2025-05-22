import librosa

def extract_mfcc(file_path, n_mfcc=13, duration=5):
    y, sr = librosa.load(file_path, duration=duration)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc.T
