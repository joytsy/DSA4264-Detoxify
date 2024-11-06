# Data Processing

_This subsection explains how we collected, cleaned, and processed our data, and how we utilized Kedro to manage these tasks._

Cleaning:

To label a subset of 400,000 comments, we utilized OpenAI's GPT-4o mini model, which demonstrated superior performance in aligning with our classification definitions compared to other models such as Mistral-7B-Instruct-v0.3 and Meta-Llama-3-8B-Instruct. We conducted labeling in batches of 80,000 comments, ensuring consistent class distributions across batches.
