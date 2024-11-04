import streamlit as st
import torch
import pandas as pd
import random
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import matplotlib.pyplot as plt

# Load the model and tokenizer
model_save_path = "./model-1/distilbert/model/multilingual_distilbert_model_5k.pth"
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-multilingual-cased", num_labels=7
)
# Load the model weights securely
model.load_state_dict(
    torch.load(model_save_path, map_location=torch.device("cpu"), weights_only=True)
)
model.eval()

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-multilingual-cased")

# Device (CPU, CUDA, or MPS)
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_built() and torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

model.to(device)

# Class labels
class_labels = [
    "No Hate/Toxic",
    "Toxic 1",
    "Toxic 2",
    "Toxic 3",
    "Hate 1",
    "Hate 2",
    "Hate 3",
]

# Label styles for the classification result box
label_styles = {
    "No Hate/Toxic": {
        "background_color": "#d4edda",
        "text_color": "#155724",
        "icon": "✅",
    },
    "Toxic 1": {"background_color": "#fff3cd", "text_color": "#856404", "icon": "⚠️"},
    "Toxic 2": {"background_color": "#ffecb3", "text_color": "#b35900", "icon": "⚠️"},
    "Toxic 3": {"background_color": "#ffcc80", "text_color": "#b35900", "icon": "❗"},
    "Hate 1": {"background_color": "#f8d7da", "text_color": "#721c24", "icon": "⚠️"},
    "Hate 2": {"background_color": "#f5b7b1", "text_color": "#721c24", "icon": "⚠️"},
    "Hate 3": {"background_color": "#e57373", "text_color": "#ffffff", "icon": "❗"},
}

# Positive feedback messages for "No Hate/Toxic"
positive_messages = [
    "Keep it going! Your words spread positivity. 😊",
    "Great job! Your comment is respectful and constructive. 👍",
    "Wonderful! Your message promotes a healthy conversation. 🌟",
    "Way to go! Your words make the world a better place. 💚",
]

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# Streamlit app with custom CSS for centralized layout
st.set_page_config(layout="centered", page_title="Lion Guard Pro Max")

# Custom CSS for interactive, tech-style app title with a highly apparent gradient scrolling effect
st.markdown(
    """
    <style>
    .title {
        font-size: 50px;
        font-weight: 700;
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        letter-spacing: 2px;
        margin-bottom: 20px;
        background: linear-gradient(90deg, #FF0000, #FF8C00, #FFD700, #FF8C00, #FF0000);
        background-size: 400% auto; /* Further increased size for a more dramatic effect */
        color: #FFF; /* Text color set to white for high contrast */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientScroll 5s ease infinite; /* Slower and smoother animation */
    }
    @keyframes gradientScroll {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    .classification-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 150px;
        font-size: 28px;
        font-weight: bold;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
        margin-top: 20px;
    }
    .classification-box:hover {
        transform: scale(1.05);
    }
    .feedback-text {
        text-align: center;
        font-size: 18px;
        margin-top: 20px;
    }
    .stTextArea textarea {
        font-size: 16px;
        height: 150px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Interactive, tech-style app title with a highly apparent gradient scrolling effect
st.markdown("<div class='title'>Lion Guard Pro Max</div>", unsafe_allow_html=True)

# Sidebar-based navigation menu
page = st.sidebar.selectbox("Navigate to", ["Classify Text", "Analysis"])

# "Classify Text" Page with Tabs
if page == "Classify Text":
    st.title("Classify Text")
    tab1, tab2, tab3 = st.tabs(["Manual Classification", "Upload CSV", "History"])

    # Tab 1: Manual Classification
    with tab1:
        st.write(
            "Enter a comment below, and the model will classify it as toxic or non-toxic with visual feedback."
        )

        # Centralized text input
        user_input = st.text_area("Type your comment here:")

        # Button and centralized output
        if st.button("Classify"):
            if user_input:
                # Tokenize and preprocess the input
                inputs = tokenizer(
                    user_input,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=128,
                )
                input_ids = inputs["input_ids"].to(device)
                attention_mask = inputs["attention_mask"].to(device)

                # Make prediction
                with torch.no_grad():
                    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                    logits = outputs.logits

                # Get the predicted class
                predicted_class = torch.argmax(logits, dim=1).item()
                predicted_label = class_labels[predicted_class]

                # Get the corresponding styles for the classification box
                styles = label_styles[predicted_label]
                background_color = styles["background_color"]
                text_color = styles["text_color"]
                icon = styles["icon"]

                # Display the classification result in a styled box
                st.markdown(
                    f"<div class='classification-box' style='background-color: {background_color}; color: {text_color};'>"
                    f"{icon} Predicted label: {predicted_label}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                # Display feedback as regular text (no box)
                if predicted_label == "No Hate/Toxic":
                    st.markdown(
                        f"<div class='feedback-text' style='color: {text_color};'>{random.choice(positive_messages)}</div>",
                        unsafe_allow_html=True,
                    )
                elif "1" in predicted_label:
                    st.markdown(
                        f"<div class='feedback-text' style='color: {text_color};'>Caution: This comment may contain mildly offensive language.</div>",
                        unsafe_allow_html=True,
                    )
                elif "2" in predicted_label:
                    st.markdown(
                        f"<div class='feedback-text' style='color: {text_color};'>Warning: This comment contains harmful language and may be considered offensive.</div>",
                        unsafe_allow_html=True,
                    )
                elif "3" in predicted_label:
                    st.markdown(
                        f"<div class='feedback-text' style='color: {text_color};'>🚨 Emergency: High-intensity toxic or hate speech detected! Immediate review is recommended.</div>",
                        unsafe_allow_html=True,
                    )

                # Add to history
                st.session_state.history.append(
                    {"text": user_input, "label": predicted_label}
                )
            else:
                st.write("Please enter a comment before clicking 'Classify'.")
        # Collapsible model information on the right
        with st.expander("Model Information", expanded=False):
            st.markdown(
                "<h5 style='font-family: Arial, sans-serif; font-size: 16px;'>Model Information</h5>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'>This app uses a fine-tuned Multilingual DistilBERT model for classifying comments into different categories of speech.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h6 style='font-family: Arial, sans-serif; font-size: 16px;'>Base Model</h6>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'>DistilBERT (multilingual)</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h6 style='font-family: Arial, sans-serif; font-size: 16px;'>Fine-tuning Data</h6>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'>15,000 rows per class</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h6 style='font-family: Arial, sans-serif; font-size: 16px;'>Classification Explanation</h6>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>Toxic Speech</strong>: Targets non-sensitive groups, such as political views, professions, lifestyle choices, objects, or places.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>Hate Speech</strong>: Targets sensitive groups, which are defined below.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h6 style='font-family: Arial, sans-serif; font-size: 16px;'>Sensitive Groups</h6>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <ul style='font-family: Arial, sans-serif; font-size: 14px;'>
                    <li>Nationality</li>
                    <li>Race</li>
                    <li>Ethnicity</li>
                    <li>Religion</li>
                    <li>Gender</li>
                    <li>Sexual Orientation</li>
                    <li>Disability</li>
                    <li>Skin Colour</li>
                    <li>Age</li>
                    <li>Generational Group (e.g., Boomers, Gen X, Gen Y, Gen Z)</li>
                    <li>Socio-economic Status</li>
                    <li>Immigration Status</li>
                </ul>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h6 style='font-family: Arial, sans-serif; font-size: 16px;'>Classes and Definitions</h6>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>No Hate/Toxic</strong>: Respectful or constructive statements, even if slightly critical or negative.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>Toxic 1</strong>: Mildly harmful language, such as negative complaints.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>Toxic 2</strong>: Explicitly harmful language, such as insults or mocking.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>Toxic 3</strong>: Incitement of harm or violence, such as harassment.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>Hate 1</strong>: Negative stereotypes or biases targeting sensitive groups.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>Hate 2</strong>: Discriminatory language that excludes or denies rights to sensitive groups.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-family: Arial, sans-serif; font-size: 14px;'><strong>Hate 3</strong>: Calls for harm or violence directed at sensitive groups.</p>",
                unsafe_allow_html=True,
            )

    # Tab 2: Upload CSV for Batch Classification
    with tab2:
        st.write(
            "Upload a CSV file containing text data to classify. The file must have a 'text' column."
        )
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)

            if "text" not in df.columns:
                st.error("The CSV file must contain a 'text' column.")
            else:
                st.write("Classifying text data...")

                # Classify each row in the 'text' column
                classifications = []
                for text in df["text"]:
                    inputs = tokenizer(
                        text,
                        return_tensors="pt",
                        truncation=True,
                        padding=True,
                        max_length=128,
                    )
                    input_ids = inputs["input_ids"].to(device)
                    attention_mask = inputs["attention_mask"].to(device)

                    with torch.no_grad():
                        outputs = model(
                            input_ids=input_ids, attention_mask=attention_mask
                        )
                        logits = outputs.logits

                    predicted_class = torch.argmax(logits, dim=1).item()
                    predicted_label = class_labels[predicted_class]
                    classifications.append(predicted_label)

                    # Add to history
                    st.session_state.history.append(
                        {"text": text, "label": predicted_label}
                    )

                # Add classifications to DataFrame and display
                df["classification"] = classifications
                st.write("Classification completed!")
                st.dataframe(df)

                # Option to download the results
                st.download_button(
                    label="Download Results",
                    data=df.to_csv(index=False),
                    file_name="classified_text.csv",
                    mime="text/csv",
                )

    # Tab 3: History of Past Classifications
    with tab3:
        st.write("History of past classifications made during this session.")
        if not st.session_state.history:
            st.write("No past classifications yet.")
        else:
            for item in st.session_state.history:
                st.write(f"**Text**: {item['text']}")
                st.write(f"**Classification**: {item['label']}")
                st.write("---")  # Separator line between history items

# "Analysis" Page with Updated Tabs
elif page == "Analysis":
    st.title("Analysis Overview")

    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview", "Frequency Trend", "Topic Modeling", "Upload CSV"]
    )

    # Tab 1: Overview
    with tab1:
        st.write("Overview of the classification results and insights.")
        if "classified_df" in st.session_state:
            df = st.session_state.classified_df
            st.write("Here's a summary of the classified data:")
            st.dataframe(df.head())
        else:
            st.write(
                "Please upload a CSV file in the 'Upload CSV' tab to start the analysis."
            )

    # Tab 2: Frequency Trend Analysis
    with tab2:
        st.write("Frequency Trend Over the Years")
        if "classified_df" in st.session_state:
            df = st.session_state.classified_df
            # Assuming the dataset has a 'year' column for trend analysis
            if "year" in df.columns:
                trend_data = (
                    df.groupby(["year", "classification"]).size().unstack(fill_value=0)
                )
                st.write("Frequency of classifications over the years:")
                # Plot the trend
                fig, ax = plt.subplots()
                trend_data.plot(ax=ax)
                ax.set_xlabel("Year")
                ax.set_ylabel("Frequency")
                ax.set_title("Classification Frequency Trend Over the Years")
                st.pyplot(fig)
            else:
                st.error("The dataset must contain a 'year' column for trend analysis.")
        else:
            st.write(
                "Please upload a CSV file in the 'Upload CSV' tab to start the analysis."
            )

    # Tab 3: Topic Modeling
    with tab3:
        st.write("Frequency of Hate/Toxic Speech by Topic")
        if "classified_df" in st.session_state:
            df = st.session_state.classified_df
            # Assuming the dataset has a 'topic' column
            if "topic" in df.columns:
                topic_data = (
                    df.groupby(["topic", "classification"]).size().unstack(fill_value=0)
                )
                st.write("Frequency of classifications by topic:")
                # Plot topic frequency
                fig, ax = plt.subplots()
                topic_data.plot(kind="bar", stacked=True, ax=ax)
                ax.set_xlabel("Topic")
                ax.set_ylabel("Frequency")
                ax.set_title("Frequency of Hate/Toxic Speech by Topic")
                st.pyplot(fig)
            else:
                st.error(
                    "The dataset must contain a 'topic' column for topic modeling."
                )
        else:
            st.write(
                "Please upload a CSV file in the 'Upload CSV' tab to start the analysis."
            )

    # Tab 4: Upload CSV for Analysis
    with tab4:
        st.write("Upload a CSV file for classification and analysis.")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file:
            # Read CSV and classify all text
            df = pd.read_csv(uploaded_file)
            if "text" not in df.columns:
                st.error("The CSV file must contain a 'text' column.")
            else:
                st.write("Classifying text data...")
                # Classify each row in the 'text' column
                classifications = []
                for text in df["text"]:
                    inputs = tokenizer(
                        text,
                        return_tensors="pt",
                        truncation=True,
                        padding=True,
                        max_length=128,
                    )
                    input_ids = inputs["input_ids"].to(device)
                    attention_mask = inputs["attention_mask"].to(device)

                    with torch.no_grad():
                        outputs = model(
                            input_ids=input_ids, attention_mask=attention_mask
                        )
                        logits = outputs.logits

                    predicted_class = torch.argmax(logits, dim=1).item()
                    predicted_label = class_labels[predicted_class]
                    classifications.append(predicted_label)

                # Add classifications to DataFrame and display
                df["classification"] = classifications
                st.write("Classification completed!")
                st.dataframe(df)

                # Store the classified DataFrame for further analysis
                st.session_state.classified_df = df

                # Option to download the results
                st.download_button(
                    label="Download Results",
                    data=df.to_csv(index=False),
                    file_name="classified_text.csv",
                    mime="text/csv",
                )


# 5k
# i love the weather today (No Hate/Toxic)
# i will never recruit indians into my company (Hate 1)
# you are a damn bloody useless gay, dont you step foot into my place (Hate 2)
# deport all the useless migrants back to their home, if they dont leave asap, i will destroy them (Hate 3)
# It's the department, want to stir shit also cannot stir properly (Toxic 1)
# you are such a loser in life (Toxic 2)
# you are such a loser in life, get out of this place or else i will kick you (Toxic 3)

# 15k
# i love the weather today (No Hate/Toxic)
# i will never recruit indians into my company (Hate 1)
# you are a damn bloody useless gay, dont you step foot into my place (Hate 2)
# the jews better get out of our country, or else i will kick them out (Hate 3)
# It's the department, want to stir shit also cannot stir properly (Toxic 1)
# you are such a loser in life (Toxic 2)
# you are such a loser in life, get out of my face, or else i will destroy you (Toxic 3)
