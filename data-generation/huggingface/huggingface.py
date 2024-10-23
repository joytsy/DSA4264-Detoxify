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

question = """i love the weather today"""
template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
“””
You are an expert annotator. Your task is to classify the following text into one of the categories below. The categories reflect increasing intensity levels, with higher numbers indicating greater severity of hate or toxic speech. There is a category for "No Hate/Toxic," which covers neutral or positive speech with no harmful content. The classification is based on the explicit language used in the comment, without considering the speaker's intent or context.

Sensitive Groups for Hate and No Hate/Toxic Speech:
Only groups defined by the following characteristics are considered sensitive groups. If the group does not fall into one of these categories, it is not a sensitive group, and the speech should be classified as Toxic if harmful:
- Nationality (e.g., Americans, Singaporeans, Canadians, Mexicans, Chinese)
- Race (e.g., Black, White, Asian, Indigenous peoples)
- Ethnicity (e.g., Jewish, Arab, Han Chinese, Latinx, Kurds)
- Religion (e.g., Muslims, Christians, Hindus, Jews, Buddhists)
- Gender (e.g., Men, Women, Non-binary)
- Sexual orientation (e.g., Gay, Lesbian, Bisexual, Asexual, Pansexual)
- Disability (e.g., Individuals with physical disabilities, Individuals with cognitive impairments, Individuals with mental health conditions, Individuals with visual or hearing impairments)
- Skin colour (e.g., Dark-skinned, Light-skinned, Brown-skinned, Pale-skinned individuals)
- Age (e.g., Children, Adolescents, Elderly, Middle-aged individuals)
- Generational group (e.g., Boomers, Gen X, Gen Y, Gen Z)
- Socio-economic status (e.g., Low-income individuals, Middle-class, Wealthy individuals, Working-class)
- Immigration status (e.g., Refugees, Asylum seekers, Immigrants, Foreign workers, Undocumented immigrants)

Non-Sensitive Groups for Toxic and No Hate/Toxic Speech:
Any group, thing, species, surroundings, or entity not defined by the above sensitive characteristics is considered a non-sensitive group. This includes:
- Political views, professions, beliefs, lifestyle choices (e.g., antivaxxers, wumao, gamers)
- Objects, animals, places, environmental elements, or any other non-human categories
If a statement targets one of these non-sensitive groups, it should be classified as Toxic rather than Hate.

Hate Speech Categories (targeting sensitive groups):
1. Hate 1: Bias and prejudice — Expressing negative stereotypes, generalizations, or biases toward sensitive groups. The focus is on harmful perceptions or attitudes, without any exclusion or incitement.
2. Hate 2: Discrimination — Exclusion or unfair treatment of sensitive groups through statements that imply denial of rights or access, without inciting harm.
3. Hate 3: Threats and violence — Inciting harm, issuing threats, or calling for action against sensitive groups.

Toxic Speech Categories (targeting non-sensitive groups, individuals, things, surroundings, species, or entities):
4. Toxic 1: Negative complaints or expressions of dissatisfaction that contain mildly harmful or disrespectful language. These statements express unwarranted blame, criticism, or negativity that goes beyond neutral discourse, making them demeaning or unnecessarily critical. But it does not escalate to direct insults or threats.
5. Toxic 2: Clear insults, sarcasm, or mocking directed at individuals, groups, things, surroundings, or entities that is explicitly harmful or demeaning.
6. Toxic 3: Harassment or encouragement of harm or violence, directed at individuals, groups, things, surroundings, or entities. This includes statements that incite harm or abusive behavior, whether directed at people or non-human entities.

No Hate/Toxic (targeting any group):
Positive, neutral, or constructive statements with no harmful or toxic elements. This category includes comments with mild negativity or frustration, lighthearted joke, casual observations, playful sarcasm, concerns, warnings or light teasing, as long as they are not intended to insult or demean. These statements should be classified as No Hate/Toxic if they remain respectful or constructive, even if slightly critical or negative.

Instructions:
1. Identify the target: Determine who or what the comment is addressing. Is it directed at a specific group, individual, thing, species, or surroundings?

2. Determine group sensitivity: Based on the characteristics provided, decide if the target  is in the sensitive group.
   - If the target involves any sensitive characteristic strictly in this list: nationality, race, ethnicity, religion, gender, sexual orientation, disability, skin colour, age, generational group, socio-economic status and immigration status. Proceed to the Hate or No Hate/Toxic categories.
   - If the target does not involve any sensitive characteristic, proceed to the Toxic or No Hate/Toxic categories.

3. Analyze the language and classify the comment:
   - **Classify the comment as a whole based solely on the overall meaning, not individual words**. Do not classify the statement as Toxic or Hate just because it contains negative words or phrases. Focus on the overall intent and meaning of the comment.
   - **Hate categories** (for sensitive groups):
     - Hate 1 (Bias and Prejudice): Negative generalizations, stereotypes, or biases toward the sensitive group. Focus on harmful perceptions or attitudes without excluding or denying access to rights or opportunities.
     - Hate 2 (Discrimination): Statements that imply exclusion, denial of access, or rights for the sensitive group. Any language implying exclusion from resources, jobs, services, or rights should be prioritized as Hate 2.
     - Hate 3 (Incitement of Harm or Violence): Direct threats or calls to harm the sensitive group.

   - **Toxic categories** (for non-sensitive groups, individuals, things, surroundings, species, or entities):
     - Toxic 1: Negative complaints or expressions of dissatisfaction that contain mildly harmful or disrespectful language. These statements express unwarranted blame, criticism, or negativity that goes beyond neutral discourse, making them demeaning or unnecessarily critical. But it does not escalate to direct insults or threats.
     - Toxic 2: Clear insults, sarcasm, or mocking directed at individuals, things, surroundings, species, or entities that is explicitly harmful or demeaning.
     - Toxic 3: Harassment or encouragement of harm or violence, directed at individuals, things, surroundings, species, or entities. This includes statements that incite harm or abusive behavior, whether directed at people or non-human entities.

   - **No Hate/Toxic** (for any group):
     - Positive, neutral, or constructive statements with no harmful or toxic elements. This category includes comments with mild negativity or frustration, lighthearted jokes, casual observations, playful sarcasm, concerns, warnings, or light teasing, as long as they are not intended to insult or demean. These statements should be classified as No Hate/Toxic if they remain respectful or constructive, even if slightly critical or negative.

Output:
- Sensitive Group: Yes/No
- Classification:
- Reasoning: Provide reasoning for the classification based on the specific example, similar to the format below:

Example:
- Sensitive Group: Yes
- Classification: Hate 1
- Reasoning: This statement targets a sensitive group (expats, based on nationality/immigration status). It includes bias and negative generalizations, stereotyping their treatment, and suggests exclusion.

Examples:

- Example 1: "Expats in Singapore always expect preferential treatment in jobs and housing."
   - Sensitive Group: Yes
   - Classification: Hate 1
   - Reasoning: This statement targets a sensitive group (expats, based on nationality/immigration status). It includes bias and negative generalizations, stereotyping their expectations of their treatment.

- Example 2: "I don't let Indians come to my restaurant because they are smelly."
   - Sensitive Group: Yes
   - Classification: Hate 2
   - Reasoning: This statement targets a sensitive group (Indians, based on ethnicity). It expresses negative generalizations and exclusion by denying Indians from accessing the restaurant, demeaning the group, implying unfair treatment without inciting violence.

- Example 3: "Gen Zs don't belong here. If they don't leave, I will kill them."
   - Sensitive Group: Yes
   - Classification: Hate 3
   - Reasoning: This statement targets a sensitive group (Gen Zs, based on their generational group). It incites harm and issues a direct threat, calling for violence, which makes it a Hate 3 classification.

- Example 4: "Aiyoh, why GST keep going up ah? Everything more expensive, but got see any improvement or not?"
   - Sensitive Group: No
   - Classification: Toxic 1
   - Reasoning: This statement does not target a sensitive group. It is a general complaint about government policy (GST) without targeting any individual or group, classifying it as Toxic 1.

- Example 5: "Wah, that TikTok employee damn smart ah? Come up with such a stupid idea—clap for him sia."
   - Sensitive Group: No
   - Classification: Toxic 2
   - Reasoning: This statement does not target a sensitive group. It mocks and uses sarcasm towards an individual (the TikTok employee) without any direct threat or incitement of harm, making it Toxic 2.

- Example 6: "No one will care if that army guy dies, he should kill himself."
   - Sensitive Group: No
   - Classification: Toxic 3
   - Reasoning: This statement does not target a sensitive group. It encourages harm or violence towards an individual (the army guy), making it a severe and harmful statement, classifying it as Toxic 3.

- Example 7: "Deep breathe, deep breathe, break down into smaller torturous and manageable steps. You got this."
   - Sensitive Group: No
   - Classification: No Hate/Toxic
   - Reasoning: This statement does not target a sensitive group. Even though "torturous" is a negative word but it is a positive and supportive comment as a whole, classifying it as No Hate/Toxic.

Output:
Sensitive Group: (Yes/No)
Classification: (e.g., "No Hate/Toxic", "Hate 1", etc)
Reasoning:
<|eot_id|><|start_header_id|>user<|end_header_id|>
Text: "{question}"
<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""


prompt = PromptTemplate(input_variables=["question"], template=template)

chain = chain = prompt | llm

llm_response = chain.invoke(question)

print(llm_response)
