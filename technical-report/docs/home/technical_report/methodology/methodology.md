# Methods Overview

<!-- ## 3.1 Technical Assumptions

_In this subsection, you should set out the assumptions that are directly related to your model development process. Some general categories include:_

- _How to define certain terms as variables_
- _What features are available / not available_
- _What kind of computational resources are available to you (ie on-premise vs cloud, GPU vs CPU, RAM availability)_
- _What the key hypotheses of interest are_
- _What the data quality is like (especially if incomplete / unreliable)_ -->

_In this subsection, we outline the overarching approach to our project, detailing the rationale behind our intensity-based classification system and the steps taken to maximize our analysis within the constraints of limited computational resources._

Our analysis of Reddit comments aimed to identify trends in hate and toxic speech over time, with a focus on understanding the intensity of such language. We developed a custom multiclass classification framework to go beyond binary distinctions, providing a deeper understanding of how hateful and toxic content manifests. To ensure maintainability and reproducibility, we used [Kedro (version 0.19.8)](data-processing/index.md#kedro) to organize our data science workflows efficiently.

## 1 Technical Assumptions

The core assumptions driving our model development, particularly those linked to our novel classification approach and data handling include:

**Custom Class Definitions:** We intentionally designed a multiclass framework to capture varying intensities of hate and toxic speech. Our classifications are intended to differentiate between sensitive group-directed hate speech (Hate 1, Hate 2, Hate 3) and non-sensitive toxic speech (Toxic 1, Toxic 2, Toxic 3). This approach allows for a nuanced analysis of the severity and impact of different text. The definitions shown below were meticulously crafted to account for both subtle and overt forms of disrespect and harm.

**Feature Availability:** We used text content as our primary feature, enhanced with embeddings from multilingual DistilBERT to handle Singapore's linguistic diversity. This decision was critical to capturing the multilingual nature of our dataset, balancing resource limitations with the need for comprehensive language coverage.

**Computational Resources:** Due to limited access to GPUs, we opted for DistilBERT over a full BERT classification model, which still allowed us to conduct efficient analysis. We restricted our analysis on text with length inclusive of 5 to 50 words, and found this reasonable since it was inclusive of the typical Reddit post length.

**Hypotheses of Interest:** We hypothesized that both the frequency and intensity of hate and toxic language would increase over time, with intensity measured according to our custom-defined categories.

**Data Quality:** Our dataset varied in quality, requiring rigorous preprocessing to manage noise, inconsistencies, and class imbalances. Due to the large size of the origial dataset, we assume that our measures taken to obtain a balanced subset for analysis is justified.

## 2 Class Definitions

### Sensitive Group Classification

We first determine if a comment refers to a sensitive group based on characteristics such as nationality, race, ethnicity, religion, gender, sexual orientation, disability, skin color, age, generational group, socio-economic status, or immigration status. Text mentioning any of these characteristics explicitly will be classified as Hateful, not Toxic.

### Language Intensity Classification

Subsequently, text will be classified into one of the 7 categories below:

1. Hate 1: Text containing bias or generalizations without exclusion or incitement.
2. Hate 2: Text that add exclusion or denial of rights to sensitive groups, including denial of access, rights, or opportunities based on group characteristics.
3. Hate 3: Text that incite harm or make threats.
4. Toxic 1: Text containing mild complaints or disrespect without direct insults or threats.
5. Toxic 2: Text containing clear insults, sarcasm, or mocking, focusing on humiliation or belittling.
6. Toxic 3: Text containing harassment or encouragement of harm.
7. No Hate/Toxic: Neutral or constructive comments, including mild criticism or playful sarcasm.
