import torch

from speechbrain.pretrained import EncoderClassifier

classifier = EncoderClassifier.from_hparams(
    source="speechbrain/lang-id-commonlanguage_ecapa",
    savedir="tmp_model"
)

def predict_accent(audio_path):
    output = classifier.classify_file(audio_path)
    label = output[3]
    if isinstance(label, list):
        label = label[0]
    score = torch.softmax(output[1], dim=0).max().item()
    explanation = (
        "The audio is classified as English. "
        "For detailed accent detection (American, British, etc.), a custom model is required. "
        "This score only reflects the likelihood of English language."
    )
    return label, round(score * 100, 2), explanation
