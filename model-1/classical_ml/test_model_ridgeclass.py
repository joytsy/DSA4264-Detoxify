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
    "Oh how I miss my Batam masseuse",
    "This cb china every time want to spread their fking virus to everyone.",
    "But, we need FTs to do the jobs that SGporeans can't do! If being stupid is the requirement, then indeed we are short of manpower.",
    "teachers pushing their religious values b4 and go on a tangent and rant about LGBTQ please report them if you see that happening and feel safe enough to report. teachers doing so contravene national values such as religious harmony.",
    "I don't hire poor workers because they are all lazy and entitled.",
    "only way to deal with migrant workers is to burn their houses",
    "Gen Z parents gotta stop giving their child ridiculous name. They are only gonna get bullied when they go to school.",
    "How shitty my block has no electricity.",
    "Get the fuck outta here you bloody wumao.",
    "Indeed these aren't discriminatory. Fuck off antivaxxers, get vaccinated or get fucked.",
    "can we send these dogs to the firing squad already hope they die a terrible death.",
    "Dont overthink it, you might hurt yourself",
    "im a bbfa fcp, i got kkj!! you come nearer, i pew pew your pigu!",
    "That calls for a celebration with one scum less in this world.",
]


# Preprocess and vectorize the input
processed_samples = [preprocess(sample) for sample in new_input_data]
new_input_vectorized = vectorizer.transform(processed_samples)

# Predict using the loaded model
predictions = clf.predict(new_input_vectorized)

# Map predictions to labels
label_mapping = [
    "No Hate/Toxic",
    "Hate 1",
    "Hate 2",
    "Hate 3",
    "Toxic 1",
    "Toxic 2",
    "Toxic 3",
]
predicted_labels = [label_mapping[pred] for pred in predictions]

# Output the predictions
for sample, label in zip(new_input_data, predicted_labels):
    print(f"Input: {sample} => Predicted Label: {label}")
