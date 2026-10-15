import pickle
import numpy as np
import tensorflow as tf
class EmotionPredictor:
    def __init__(
        self,
        model_path: str = r"D:\Sentimental Analysis\Model\bigru_goemotions_model.keras",
        artifacts_path: str = r"D:\Sentimental Analysis\Model\model_artifacts.pkl",
    ):
        self.model = tf.keras.models.load_model(model_path)
        with open(artifacts_path, "rb") as f:
            artifacts = pickle.load(f)

        self.tokenizer = artifacts.get("tokenizer")
        self.max_len = artifacts.get("max_len", 70)
        self.thresholds = artifacts.get("thresholds")
        self.mapping = artifacts.get("mapping", {})

    def preprocess(self, text: str):
        sequences = self.tokenizer.texts_to_sequences([text])
        padded = tf.keras.preprocessing.sequence.pad_sequences(
            sequences, maxlen=self.max_len, padding="post", truncating="post"
        )
        return padded

    def predict(self, text: str, top_k: int = 3):
        processed_input = self.preprocess(text)
        probs = self.model.predict(processed_input, verbose=0)[0]

        predicted_emotions = []

        for c, prob in enumerate(probs):
            if prob >= self.thresholds[c]:
                emotion_name = self.mapping.get(int(c), f"Emotion_{c}")
                predicted_emotions.append((emotion_name, float(prob)))

        if len(predicted_emotions) < top_k:
            top_indices = np.argsort(probs)[::-1]
            for idx in top_indices:
                emotion_name = self.mapping.get(int(idx), f"Emotion_{idx}")
                item = (emotion_name, float(probs[idx]))
                if item not in predicted_emotions:
                    predicted_emotions.append(item)
                if len(predicted_emotions) == top_k:
                    break

        predicted_emotions.sort(key=lambda x: x[1], reverse=True)
        return predicted_emotions