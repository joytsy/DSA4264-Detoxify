import joblib
import os

# Load the model and vectorizer from the 'model' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "model", "model.pkl")
vectorizer_path = os.path.join(current_dir, "model", "tfidf_vectorizer.pkl")
label_encoder_path = os.path.join(
    current_dir, "model", "label_encoder.pkl"
)  # Assuming LabelEncoder is saved

# Load the trained SVM model, TF-IDF vectorizer, and LabelEncoder
best_model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
label_encoder = joblib.load(label_encoder_path)  # Load the saved LabelEncoder


class Detector:
    def __init__(self):
        # The model, vectorizer, and label encoder are loaded when this class is instantiated
        self.model = best_model
        self.vectorizer = vectorizer
        self.label_encoder = label_encoder

    def predict(self, text):
        # Transform the input text using the TF-IDF vectorizer
        text_tfidf = self.vectorizer.transform([text])
        # Predict the class label using the SVM model
        prediction = self.model.predict(text_tfidf)
        # Convert the numeric prediction back to the original class label
        class_name = self.label_encoder.inverse_transform([prediction[0]])[0]
        return class_name
