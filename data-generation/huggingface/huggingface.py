import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain import PromptTemplate

load_dotenv()
hf_token = os.getenv("HF_TOKEN", None)

repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_new_tokens=250,
    temperature=0.8,
    huggingfacehub_api_token=hf_token,
)

question = """id of gxeiu21 replied to id of gxeilbl: So useless Just like your skull
id of gxej1ew replied to id of gxeiu21: Is this the stupid hill your ignorant self wishes to die on Are you just hoping ill stop calling you out
id of gxejkym replied to id of gxej1ew: Is this the stupid hill your brainless self wishes to die on Are you just hoping for me to acknowledge your projections
id of gxejqr8 replied to id of gxejkym: Go on sherlock, tell me what you think projection means. Sounds like you're using another word you know fuck all about You know... like xenophobia, culture, 'lapse of judgment' etc
id of gxek6ep replied to id of gxejqr8: If you dont stop, i will really do something to you. Sounds like you're just reusing the same vocabulary all over again because that's all you know You know... like fool, idiot, einstein etc."""
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

Examples:

Example 1:
Text: "Foreigners are taking all our jobs."
1. Identify Target: The comment targets a specific group (foreigners).
2. Assess Intensity: The comment expresses bias against this group but does not call for action.
3. Apply Hate or Toxic Levels: This qualifies as Hate 1 (bias and prejudice).
4. Final Classification: Hate 1

Example 2:
Text: "You’re an idiot, why do you even try?"
1. Identify Target: The comment targets an individual.
2. Assess Intensity: This is a direct insult aimed at belittling the person.
3. Apply Hate or Toxic Levels: This qualifies as Toxic 2 (insults and sarcasm).
4. Final Classification: Toxic 2

Example 3:
Text: "I refuse to serve Black people in my restaurant."
1. Identify Target: The comment targets a specific group (Black people).
2. Assess Intensity: The comment discriminates against this group by denying service.
3. Apply Hate or Toxic Levels: This qualifies as Hate 2 (discrimination).
4. Final Classification: Hate 2

Now, classify the following comment based on this step-by-step process. Do the chain of thought for yourself and then provide the classification as output.
<|eot_id|><|start_header_id|>user<|end_header_id|>
Text: "{question}"
<|eot_id|><|start_header_id|>assistant<|end_header_id|>'''

prompt = PromptTemplate(input_variables=["question"], template=template)

chain = chain = prompt | llm

llm_response = chain.invoke(question)

print(llm_response)
