# Model-1: Multiclass Text Classifier for Detecting Toxicity/Hatefulness

This folder contains the resources and scripts for training a multiclass text classifier to detect toxicity and hatefulness in online comments. The classifier identifies and categorizes speech into six classes: Hate 1, Hate 2, Hate 3, Toxic 1, Toxic 2, Toxic 3, and No Hate/Toxic, using various machine learning models, including classical approaches, BERT, and DistilBERT.

## Folder Structure

The `model-1` folder is organized into three subfolders, each dedicated to a different type of model: `bert`, `classical_ml`, and `distilbert`.

---

### 1. `classical_ml` Folder

This folder contains scripts for training classical machine learning models, including RidgeClassifierCV, XGBoost, Naive Bayes Classifier, and Linear SVM. Various sampling strategies are used to address class imbalance, including synthetic data generation and SMOTE.

- **Files:**
  - **classic_model1_5k.ipynb**
    Trains all classical models with each class having 5,000 samples.
    Uses synthetic data generation for upsampling lower classes and random downsampling for higher classes.
  - **classic_model1_15k.ipynb**
    Trains all classical models with each class having 15,000 samples.
    Employs synthetic data generation for upsampling and random downsampling for higher classes.
  - **classic_model1_sampling.ipynb**
    Uses SMOTE (Synthetic Minority Over-sampling Technique) for upsampling and random downsampling for balancing class distributions.
  - **test_model_ridgeclass.py**
    Script for predicting the class of a single comment using the RidgeClassifier model.

---

### 2. `bert` Folder

This folder contains a script for training a BERT-based model to classify comments based on their toxicity and hatefulness.

- **Files:**
  - **model_1_bert.ipynb**
    Training file for the BERT model, detailing the data preprocessing, model architecture, and training steps.

---

### 3. `distilbert` Folder

This folder contains scripts and utilities for working with a fine-tuned multilingual DistilBERT model. The model is used for both training and prediction tasks.

- **Files:**
  - **labelling.py**
    Script for labeling data using the fine-tuned multilingual DistilBERT model.
  - **model_1_distilbert.ipynb**
    Training script for the fine-tuned multilingual DistilBERT, outlining the model training and evaluation processes.
  - **multilingual_predict.py**
    Script for predicting the class of a single comment using the fine-tuned multilingual DistilBERT model.

---

## Data Requirements

To train the models effectively, you need to include the following datasets in each model subfolder:

1. **training_data_5k.csv**
   - Contains 5,000 samples for each class, used for balanced training with smaller datasets.
2. **training_data_15k.csv**
   - Contains 15,000 samples for each class, used for balanced training with larger datasets.
3. **training_data.csv**
   - Contains an imbalanced dataset, reflecting the natural distribution of comments across the classes.

Ensure these CSV files are placed in the `classical_ml`, `bert`, and `distilbert` folders to allow the scripts and notebooks to run as expected.

---

## Usage

- For classical machine learning models, choose the appropriate notebook (`classic_model1_5k.ipynb`, `classic_model1_15k.ipynb`, or `classic_model1_sampling.ipynb`) based on your sample size requirements and preferred sampling technique.
- For BERT, use `model_1_bert.ipynb` to train the model and fine-tune the hyperparameters as needed.
- For DistilBERT, use `labelling.py` to label your dataset, `model_1_distilbert.ipynb` to train the model, and `multilingual_predict.py` for making predictions on individual comments.

## Requirements

1. **Install Dependencies**:
   Make sure you have Python installed. Navigate to the outermost directory of the repository and install the required dependencies using:

   ```bash
   pip install -r requirements.txt
   ```

---

## Notes

- **Class Imbalance Handling**: Various techniques, such as synthetic data generation and SMOTE, have been applied to deal with class imbalances and improve model performance.
- **Fine-tuning and Optimization**: The BERT and DistilBERT models are fine-tuned on a large corpus of multilingual comments, making them suitable for a variety of online toxicity and hatefulness detection tasks.
