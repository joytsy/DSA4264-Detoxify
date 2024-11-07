import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("wordnet")

# Initialize lemmatizer and stop words
lemmatizer = WordNetLemmatizer()


def preprocess(text):
    # Tokenization
    words = word_tokenize(text.lower())
    # Remove punctuation and non-alphabetic tokens
    words = [word for word in words if word.isalpha()]
    # Lemmatization
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)


# Load the saved model and vectorizer (relative paths)
clf = joblib.load(
    r"C:\Users\user\OneDrive - National University of Singapore\Desktop\Y4S1\DSA4264\DSA4264-Detoxify\model-1\classicML_joyKylie\ridge_classifier_model.pkl"
)
vectorizer = joblib.load(
    r"C:\Users\user\OneDrive - National University of Singapore\Desktop\Y4S1\DSA4264\DSA4264-Detoxify\model-1\classicML_joyKylie\vectorizer.pkl"
)
print("Model and vectorizer loaded successfully.")

# Example input data (replace with your own input)
new_input_data = [
    "today is a beautiful day",
    "i love the weather today",
    "i will never recruit indians into my company",
    "you are a damn bloody useless gay, dont you step foot into my place",
    "deport all the useless migrants back to their home, if they dont leave asap, i will destroy them",
    "It's the department, want to stir shit also cannot stir properly",
    "you are such a loser in life",
    "you are such a loser in life, get out of this place or else i will kick you",
]


# Preprocess and vectorize the input
processed_samples = [preprocess(sample) for sample in new_input_data]
new_input_vectorized = vectorizer.transform(processed_samples)

# Predict using the loaded model
predictions = clf.predict(new_input_vectorized)

# Map predictions to labels
label_mapping = [
    "No Hate/Toxic",
    "Toxic 1",
    "Toxic 2",
    "Toxic 3",
    "Hate 1",
    "Hate 2",
    "Hate 3",
]
predicted_labels = [label_mapping[pred] for pred in predictions]

# Output the predictions
for sample, label in zip(new_input_data, predicted_labels):
    print(f"Input: {sample} => Predicted Label: {label}")
