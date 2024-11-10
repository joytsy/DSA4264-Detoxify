# LionGuard Pro Max Frontend

Welcome to the **LionGuard Pro Max** frontend! This is the user interface for an advanced web application designed to classify and analyze toxic and hateful comments using state-of-the-art machine learning models. The frontend leverages **Streamlit** to provide an interactive and visually appealing experience.

## Features

- **Classify Text**: Manually enter comments and get instant feedback on their toxicity or hate levels, complete with visual indicators.
- **Upload CSV**: Upload a CSV file containing thousands of comments to classify in bulk. Receive automated insights and downloadable results.
- **Automated Analysis**: Explore in-depth data analysis, including frequency trends and topic modeling, to gain actionable insights.
- **Model Information**: Learn about the machine learning model and the classification definitions for a better understanding of the system.

## Folder Structure

The `frontend` folder is organized as follows:

- **Home.py**: The main file to launch the application, providing an overview of the app's features and guiding users on how to navigate.
- **pages/**: Contains the primary pages for the app:
  - **1_Classify_Text.py**: A page dedicated to text classification, with options for manual input, CSV upload, and a history of past classifications.
  - **2_Analysis.py**: A comprehensive analysis section to explore trends, topics, and solutions for managing toxic and hateful comments.
- **model/**: Contains the fine-tuned Multilingual DistilBERT model for text classification.
  - **multilingual_distilbert_model_5k.pth**: The PyTorch model file.

## How to Run

1. **Install Dependencies**:
   Make sure you have Python installed. Navigate to the outermost directory of the repository and install the required dependencies using:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**:
   Navigate to the frontend folder and run the Streamlit app:

   ```bash
   streamlit run Home.py
   ```

3. **Access the App**:
   Open your browser and go to the URL provided by Streamlit, typically <http://localhost:8501>.

## Workflow Overview

- **Text Classification**:

  - Access the **Classify Text** page.
  - Input text manually or upload a CSV file.
  - View classification results with explanations.

- **Automated Analysis**:

  - Navigate to the **Analysis** page.
  - Upload your dataset for detailed insights.
  - Explore trends, identify topics, and download results for reporting.

## Classification Definitions

The app uses a fine-tuned Multilingual DistilBERT model to classify comments into the following categories:

- **No Hate/Toxic**: Respectful or constructive statements.
- **Toxic 1, 2, 3**: Varying levels of toxic language, from mild complaints to explicit harm or harassment.
- **Hate 1, 2, 3**: Varying levels of hate speech, from stereotypes to calls for violence, specifically targeting sensitive groups.

For more detailed definitions and explanations, refer to the "Model Information" section in the app.

## Notes

- **Data Privacy**: Ensure that any uploaded data complies with privacy regulations and guidelines.
- **Performance**: The app may take longer to classify large datasets, depending on your system's resources.

## Contributing

Contributions are welcome! If you'd like to improve the app or add new features, feel free to fork the repository and create a pull request.

---

Enjoy using **LionGuard Pro Max** and experience the future of comment moderation and analysis today!
