import os
import pandas as pd
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain import PromptTemplate

# Load environment variables
load_dotenv()
hf_token = os.getenv("HF_TOKEN", None)

# Initialize the HuggingFace model endpoint
repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_new_tokens=250,
    temperature=0.8,
    huggingfacehub_api_token=hf_token,
)

# Template for the classification task
template = '''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
prompt = """
You are an expert annotator. Your task is to classify the following text into one of the following categories:

1. No Hate/Toxic: The comment contains no hate or toxic speech.
2. Hate 1: Bias and prejudice (e.g., attitudes or beliefs about a group).
3. Hate 2: Discrimination (expressing dislike or exclusion but without a call to action).
4. Hate 3: Threats and violence (contains direct threats, incitement to violence, or serious harm).
5. Toxic 1: Baseless complaints (complaints or frustrations without direct harm).
6. Toxic 2: Insults or sarcasm directed at someone (humiliation or belittling without inciting violence).
7. Toxic 3: Insults with high level of hostility, aggressive, harassment or threats of harm (incitement to self-harm or targeted harassment).

Please classify each comment based on the most severe form of speech present, either hate or toxic speech (but not both). Follow the step-by-step reasoning process below to ensure accurate classification.

Definitions:

- Hate speech targets specific groups based on attributes like race, ethnicity, religion, gender, sexual orientation, disability, or other personal characteristics.
  - Hate 1: Bias and prejudice against a group (e.g., "Foreigners are taking all our jobs").
  - Hate 2: Discrimination, denying opportunities or service based on group membership (e.g., "I won’t serve anyone who looks Indian").
  - Hate 3: Threats or incitement to violence against a group (e.g., "If immigrants don’t leave, I will make them suffer").

- Toxic speech refers to general hostility or negativity that may not be tied to specific groups but creates a harmful environment.
  - Toxic 1: Baseless complaints or frustrations (e.g., "This job is a waste of time").
  - Toxic 2: Insults or sarcasm directed at someone, humiliation or belittling without inciting violence (e.g., "You’re so stupid").
  - Toxic 3: Insults with high level of hostility, aggressive, harassment or threats of harm (e.g., "Go end your life, no one cares about you").

Step-by-Step Classification Process:

1. Identify Target: Determine whether the text targets a specific group or an individual (group = hate, individual = toxic).
2. Assess Intensity: Evaluate the severity of the statement. Does it express an opinion, incite discrimination, or make threats?
3. Apply Hate or Toxic Levels: Assign a label based on the most severe behavior present in the text (choose either hate or toxic, not both).
4. Final Classification: Choose the highest relevant category based on the content.

Now, classify the following comment based on this step-by-step process. Do the chain of thought for yourself and then provide the classification as output.
<|eot_id|><|start_header_id|>user<|end_header_id|>
Text: "{question}"
<|eot_id|><|start_header_id|>assistant<|end_header_id|>'''

prompt = PromptTemplate(input_variables=["question"], template=template)


# Define the function to classify each text
def classify_text(question, llm_chain):
    llm_response = llm_chain.invoke(question)
    return llm_response


# Read data using the python engine
def read_data(file_path):
    try:
        data = pd.read_csv(file_path, engine="python")
        return data
    except Exception as e:
        print(f"Failed to read data: {e}")
        return None


# Path to your CSV file
file_path = "kedro-data/data/03_primary/clean_concatenated_texts_data.csv/2024-10-08T14.12.53.065Z/clean_concatenated_texts_data.csv"

# Load your data
data = read_data(file_path)


def process_data(start_idx, end_idx, data):
    if data is None:
        print("No data to process. Exiting...")
        return

    # Initialize the LLM chain
    chain = prompt | llm

    # Create a new column to store the classifications
    if "ground_truth" not in data.columns:
        data["ground_truth"] = None

    # Iterate through the dataset within the specified range
    for idx in range(start_idx, min(end_idx, len(data))):
        row = data.iloc[idx]
        if pd.isnull(row["ground_truth"]):  # Only classify rows without a label
            print(f"Classifying row {idx}")
            question = row["text"]

            # Get classification from the model
            classification = classify_text(question, chain)

            if classification is not None:
                # Store the classification result but don't save yet
                data.at[idx, "ground_truth"] = classification
            else:
                # If classification fails, save progress and exit
                print(
                    f"Classification failed at row {idx}. Saving progress and stopping."
                )
                data.to_csv("classified_data_partial.csv", index=True)
                return  # Exit the loop and stop processing

    # Save the final progress after all rows are processed successfully
    data.to_csv("classified_data_final.csv", index=True)
    print("Final progress saved.")


# Specify the index range
start_idx = 0  # Replace with your start index
end_idx = 499  # Replace with your end index

# Process the data within the specified index range
process_data(start_idx, end_idx, data)
