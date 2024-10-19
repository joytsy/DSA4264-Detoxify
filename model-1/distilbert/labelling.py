import torch
import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Load the fine-tuned model and tokenizer
model_save_path = r"model-1\distilbert\distilbert_model.pth"
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=7)
model.load_state_dict(torch.load(model_save_path, map_location=torch.device("cpu")))
model.eval()

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define class labels
class_labels = ["No Hate/Toxic", "Toxic 1", "Toxic 2", "Toxic 3", "Hate 1", "Hate 2", "Hate 3"]

# Step 1: Load the CSV file
csv_path = r"C:\Users\Yi Jing\Documents\Y4S1\dsa4264\DSA4264-Detoxify\kedro-data\data\03_primary\filtered_comment_data.csv"  # Update with the actual path to your CSV file
df = pd.read_csv(csv_path)[1:1000] ## change the index here

text_column = 'text' 

# Step 2: Create an empty list to store predicted labels
predicted_labels = []

# Step 3: Loop through each row in the DataFrame
for text in df[text_column]:
    # Preprocess the input (tokenization)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    # Move input tensors to the same device as the model
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # Make predictions
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits

    # Get the predicted class index
    predicted_class = torch.argmax(logits, dim=1).item()
    
    # Map predicted class index to the corresponding label
    predicted_label = class_labels[predicted_class]
    
    # Append the predicted label to the list
    predicted_labels.append(predicted_label)

# Step 4: Add the predicted labels as a new column in the DataFrame
df['predicted_label'] = predicted_labels

# Step 5: Save the updated DataFrame to a new CSV file
df.to_csv('predicted_labels_output.csv', index=False)