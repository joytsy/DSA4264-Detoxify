import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Load the fine-tuned model and tokenizer
model_save_path = "./model-1/distilbert/model/multilingual_distilbert_model_15k.pth"
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

# Custom prompt for prediction
custom_prompt = (
    "you are such a loser in life, get out of my face, or else i will destroy you"
)

# Step 1: Preprocess the input (tokenization)
inputs = tokenizer(
    custom_prompt, return_tensors="pt", truncation=True, padding=True, max_length=128
)

# Move the input tensors to the same device as the model
input_ids = inputs["input_ids"].to(device)
attention_mask = inputs["attention_mask"].to(device)

# Step 2: Make predictions
with torch.no_grad():
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    logits = outputs.logits

# Step 3: Post-process the output to get the predicted class
predicted_class = torch.argmax(logits, dim=1).item()

# Step 4: Convert the predicted class to the corresponding label
class_labels = [
    "No Hate/Toxic",
    "Toxic 1",
    "Toxic 2",
    "Toxic 3",
    "Hate 1",
    "Hate 2",
    "Hate 3",
]
predicted_label = class_labels[predicted_class]

print(f"Predicted label: {predicted_label}")

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
