# Multiclass Text Classification Model

<!-- ## 3.3 Experimental Design

_In this subsection, you should clearly explain the key steps of your model development process, such as:_

- _Algorithms: Which ML algorithms did you choose to experiment with, and why?_
- _Evaluation: Which evaluation metric did you optimise and assess the model on? Why is this the most appropriate?_
- _Training: How did you arrive at the final set of hyperparameters? How did you manage imbalanced data or regularisation?_  -->

We developed a custom multiclass text classification model tailored to encapsulate our predefined definitions of hate and toxic speech. This approach not only ensures alignment with our specific criteria but also enhances scalability by eliminating the future need to rely on external API calls for labeling, allowing us to handle datasets independently.

## 1. Data generation

The 400,000 labelled comments revealed a significant class imbalance [(Table 2)](../data-processing/index.md#dataset)

Initially, we addressed class imbalance by applying calculated class weights to `CrossEntropyLoss` and using a stratified split for balanced training, validation, and test sets. However, DistilBERT still struggled with minority classes, so we generated synthetic data to create a fully balanced dataset, eliminating the need for class weights and significantly improving model performance.

Standard techniques like [`SMOTE`](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html), undersampling, and oversampling with [`imblearn`](https://imbalanced-learn.org/stable/combine.html) proved ineffective, as identifying hate and toxic speech in Reddit text often requires nuanced attention that these methods do not capture well. To address this, we opted to synthetically generate data for classes with fewer than 15,000 examples and randomly sampled 15,000 instances from larger classes. When we tried with a lower threshold of 5,000 per class, we observed that across all models, performance was lower compared to that of 15,000. We chose the 15,000 threshold ultimately to minimize the number of classes needing synthetic data, ensuring balanced representation with minimal generation. Our approach to generate data using a template-based approach drew inspiration from [SGHateCheck](https://github.com/Social-AI-Studio/SGHateCheck).

The template-based approach was used for generating data in 4 classes - Hate 2, Hate 3, Toxic 2, and Toxic 3, by tailoring each template to match the tone and language of each category. "Hate" templates included sensitive groups and bias-driven actions, while "Toxic" templates reflected general disrespect without targeting specific groups. By combining templates with action and group lists through a Cartesian product approach, we produced diverse and contextually relevant synthetic comments that closely aligned with our classification definitions, effectively enhancing model training for underrepresented classes.

![Template generation eg](https://github.com/joytsy/DSA4264-Detoxify/blob/ff88b21654814e3a3f8b3b2fd9220bae3500e53e/technical-report/docs/home/technical_report/images/template_generation.png)

The final dataset consisted of 105,000 labelled texts. It consists of the data labelled by GPT-4o mini and data that was synthetically generated using our templates. The dataset was split into train (70%), validation (15%), and test (15%) for us to train and evaluate Distilbert and other traditional machine learning models.

## 2. DistilBERT Model

To leverage transformer-based architecture without excessive computational cost, we selected [DistilBERT](https://huggingface.co/docs/transformers/en/model_doc/distilbert), a distilled version of [BERT](https://huggingface.co/docs/transformers/en/model_doc/bert), which provides a balance of efficiency and accuracy by retaining the core transformer architecture in a more lightweight model. DistilBERT can capture nuanced linguistic features essential for hate and toxic speech classification.

### Data Preparation

The DistilBERT tokenizer, specifically the distilbert-base-multilingual-cased variant, captures word context and relationships, crucial for nuanced hate and toxic speech detection. It uses subword tokenization, enabling the model to handle slang, out-of-vocabulary words, and multilingual contexts commonly found in online text. We tokenized each text sample with this multilingual tokenizer, setting a maximum token length of 128 to balance context preservation and memory efficiency. Labels were mapped to integer values across seven predefined classes, and data loaders were configured with a batch size of 128 for efficient model training and evaluation.

### Training and Hyperparameter Tuning

DistilBERT was trained over three epochs with a learning rate of 1e-5. Dropout rates were set to 0.2 for both attention and hidden layers to reduce overfitting. The AdamW optimizer with a weight decay of 0.01 was used, and a learning rate scheduler with warmup steps (10% of total training steps) was implemented to gradually adjust the learning rate during training.

### Training Process

During each epoch, the model computed loss and accuracy across batches, with scheduler steps adjusting the learning rate. After each epoch, validation performance was evaluated, and the model with the best validation loss was saved for testing.

### Evaluation and Testing

The best-performing DistilBERT model was then evaluated on the test set, using accuracy, loss, and weighted F1 score as metrics. F1 score was particularly important to balance precision and recall across all classes, given the inherent imbalance.

## 3. Traditional Machine Learning Models

To benchmark performance, we also trained traditional machine learning models on the dataset.

1. Ridge Regression: Tuned with 5-fold cross-validation, achieving a best alpha of 4.0.

2. XGBoost: Optimized with a grid search, with best parameters of learning_rate=0.1, max_depth=5, n_estimators=100, and subsample=0.5.

3. Naive Bayes Classifier: Used as a baseline due to computational efficiency.

4. Linear SVM: Included for its performance in high-dimensional spaces but with minimal tuning.

### 3.1 Preprocessing for Traditional Models

We applied tokenization, stopword removal, lemmatization, and TF-IDF vectorization (max 5000 features) to convert text into numerical representations for traditional models. TF-IDF was chosen for its efficiency in creating sparse, interpretable feature vectors that work well with linear classifiers like Ridge and Naive Bayes. Although TF-IDF lacks contextual depth, it remains effective in capturing term importance and distinguishing words across classes, offering a suitable baseline for simpler models. Labels were mapped to integers, and the dataset was split into training, validation, and test sets using the same 70-15-15 ratio and balanced distribution applied for DistilBERT.

## 4. Evaluation

For all models, we used accuracy, loss, and weighted F1 score as evaluation metrics. The F1 score, which balances precision and recall, was critical in this project due to the multiclass nature of our task.
