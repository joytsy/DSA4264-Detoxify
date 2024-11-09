# Methods Overview

<!-- ## 3.1 Technical Assumptions

_In this subsection, you should set out the assumptions that are directly related to your model development process. Some general categories include:_

- _How to define certain terms as variables_
- _What features are available / not available_
- _What kind of computational resources are available to you (ie on-premise vs cloud, GPU vs CPU, RAM availability)_
- _What the key hypotheses of interest are_
- _What the data quality is like (especially if incomplete / unreliable)_ -->

![flow](methods.png)

<div align="center" style="font-size:  0.85em;">

Figure 2. Methodology workflow

</div>

_The methdology section consists of 5 different sections (Figure 2). In Methods Overview, we first outline the overarching approach to our project, detailing the rationale behind our intensity-based classification system and the steps taken to maximize our analysis with the computational resources we have._

Our analysis of Reddit comments aimed to identify trends in hate and toxic speech over time, with a focus on understanding the intensity of such language. We developed a custom [multiclass classification](../methodology/modelling/model1.md#multiclass-text-classification-model) framework to go beyond binary distinctions, providing a deeper understanding of how hateful and toxic content manifests. We subsequently deep-dived to analyse hate and toxic speech that were prioritised and had greater urgency to be address using [topic modelling](../methodology/modelling/model2.md#methodology-and-tools-for-analyzing-reddit-data). To ensure maintainability and reproducibility, we used [Kedro (version 0.19.8)](data-processing/index.md#11-kedro) to organize our data science workflows efficiently.

## 1. Technical Assumptions

The core assumptions driving our model development, particularly those linked to our novel classification approach and data handling include:

**Custom Class Definitions:** We intentionally designed a multiclass framework to capture varying intensities of hate and toxic speech. Our classifications are intended to differentiate between sensitive group-directed hate speech (Hate 1, Hate 2, Hate 3) and non-sensitive toxic speech (Toxic 1, Toxic 2, Toxic 3). This approach allows for a nuanced analysis of the severity and impact of different text. The definitions shown below were meticulously crafted to account for both subtle and overt forms of disrespect and harm.

**Feature Availability:** We used text content as our primary feature, enhanced with embeddings from multilingual DistilBERT to handle Singapore's linguistic diversity. This decision was critical to capturing the multilingual nature of our dataset, balancing resource limitations with the need for comprehensive language coverage.

**Computational Resources:** Due to limited access to GPUs, we opted for DistilBERT over a full BERT classification model, which still allowed us to conduct efficient analysis. We restricted our analysis on text with length inclusive of 5 to 50 words, and found this reasonable since it was inclusive of the typical Reddit post length.

**Hypotheses of Interest:** We hypothesized that both the frequency and intensity of hate and toxic language would increase over time, with intensity measured according to our custom-defined categories.

**Data Quality:** Our dataset varied in quality, requiring rigorous preprocessing to manage noise, inconsistencies, and class imbalances. Due to the large size of the origial dataset, we assume that our measures taken to obtain a balanced subset for analysis is justified.

## 2. Class Definitions

Some works adopt the concept of hate speech as being [aimed at a protected group](https://arxiv.org/abs/2405.01842). Additionally, hate and toxic speech need to be identified in a way that [prioritises those needing immediate attention](https://aclanthology.org/W19-3506.pdf). This led us to the development of a multiclass classification framswork:

### 2.1 Sensitive Group Classification

In our project, we classify a comment as referring to a sensitive group if it mentions characteristics such as nationality, race, ethnicity, religion, gender, sexual orientation, disability, skin color, age, generational group, socio-economic status, or immigration status. Our choice of groups aligns with Singapore’s legal framework against harmful speech, specifically referencing the [Maintenance of Religious Harmony Act](https://sso.agc.gov.sg/Act/MRHA1990) and [Section 298A of the Penal Code](https://sso.agc.gov.sg/Act/PC1871), which identify protected groups. Additionally, based on analysis of sample texts and discussions, we included extra groups that appeared frequently in potentially hateful comments. Text mentioning any of these characteristics explicitly will be classified as Hateful rather than Toxic.

### 2.2 Language Intensity Classification

Subsequently, text will be classified into one of the 7 categories below:

1. Hate 1: Text containing bias or generalizations without exclusion or incitement.
2. Hate 2: Text that add exclusion or denial of rights to sensitive groups, including denial of access, rights, or opportunities based on group characteristics.
3. Hate 3: Text that incite harm or make threats.
4. Toxic 1: Text containing mild complaints or disrespect without direct insults or threats.
5. Toxic 2: Text containing clear insults, sarcasm, or mocking, focusing on humiliation or belittling.
6. Toxic 3: Text containing harassment or encouragement of harm.
7. No Hate/Toxic: Neutral or constructive comments, including mild criticism or playful sarcasm.
