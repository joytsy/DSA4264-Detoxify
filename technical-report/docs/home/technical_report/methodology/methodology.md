# Methods Overview

_In this subsection, we outline the overarching approach to our project, detailing the rationale behind our intensity-based classification system and the steps taken to maximize our analysis within the constraints of limited computational resources._

Our analysis of 4.5 million Reddit comments aimed to identify trends in hate and toxic speech over time, with a focus on understanding the intensity of such language. We developed a custom multiclass classification framework to go beyond binary distinctions, providing a deeper understanding of how hateful and toxic content manifests. To ensure maintainability and reproducibility, we used Kedro (version 0.19.8) to organize our data science workflows efficiently.

## Technical Assumptions

The core assumptions driving our model development, particularly those linked to our novel classification approach and data handling include:

1. Custom Class Definitions: We intentionally designed a multiclass framework to capture varying intensities of hate and toxic speech. Our classifications differentiated between sensitive group-directed hate speech (Hate 1, Hate 2, Hate 3) and non-sensitive toxic speech (Toxic 1, Toxic 2, Toxic 3). This approach allowed for a nuanced analysis of the severity and impact of different types of language. Our definitions were meticulously crafted to account for both subtle and overt forms of disrespect and harm.
2. Feature Availability: We used text content as our primary feature, enhanced with embeddings from multilingual DistilBERT to handle Singapore's linguistic diversity. This decision was critical to capturing the multilingual nature of our dataset (check this part), balancing resource limitations with the need for comprehensive language coverage.
3. Computational Resources: Due to limited access to GPUs, we opted for DistilBERT over a full BERT model. We leveraged Kedro version 0.19.6 for our data science pipeline to ensure scalability and efficiency, managing complex tasks seamlessly.
4. Hypotheses of Interest: We hypothesized an increase in the intensity of hate and toxic language over time and sought to identify linguistic patterns associated with this trend. We aimed to understand differences in the language used for sensitive versus non-sensitive groups.
5. Data Quality: Our dataset varied in quality, requiring rigorous preprocessing to manage noise, inconsistencies, and class imbalances. When we labelled our dataset in batches of 80,000 comments at a time due to resource limitations, each batch maintained similar class distributions, justifying our use of a smaller, labeled subset of 400,000 comments to train and evaluate our models effectively.

## Class Definitions

### Sensitive Group Classification

We first determine if a comment refers to a group based on characteristics such as nationality, race, ethnicity, religion, gender, sexual orientation, disability, skin color, age, generational group, socio-economic status, or immigration status.

- Sensitive Group: Yes – If the text mentions any of these characteristics explicitly.
- Sensitive Group: No – If the text does not mention any of these characteristics.

### Language Intensity Classification

For Sensitive Groups (Hate Speech):

1.Hate 1: Statements containing bias or generalizations without exclusion or incitement.
2.Hate 2: Statements that add exclusion or denial of rights to sensitive groups, including denial of access, rights, or opportunities based on group characteristics.
3.Hate 3: Statements that incite harm or make threats.

For Non-Sensitive Groups (Toxic Speech):

4.Toxic 1: Mild complaints or disrespect without direct insults or threats.
5.Toxic 2: Clear insults, sarcasm, or mocking, focusing on humiliation or belittling.
6.Toxic 3: Harassment or encouragement of harm.

7.No Hate/Toxic: Neutral or constructive comments, including mild criticism or playful sarcasm.

<!-- ## 3.1 Technical Assumptions

_In this subsection, you should set out the assumptions that are directly related to your model development process. Some general categories include:_

- _How to define certain terms as variables_
- _What features are available / not available_
- _What kind of computational resources are available to you (ie on-premise vs cloud, GPU vs CPU, RAM availability)_
- _What the key hypotheses of interest are_
- _What the data quality is like (especially if incomplete / unreliable)_

## 3.2 Data

_In this subsection, you should provide a clear and detailed explanation of how your data is collected, processed, and used. Some specific parts you should explain are:_

- _Collection: What datasets did you use and how are they collected?_
- _Cleaning: How did you clean the data? How did you treat outliers or missing values?_
- _Features: What feature engineering did you do? Was anything dropped?_
- _Splitting: How did you split the data between training and test sets?_

## 3.3 Experimental Design

_In this subsection, you should clearly explain the key steps of your model development process, such as:_

- _Algorithms: Which ML algorithms did you choose to experiment with, and why?_
- _Evaluation: Which evaluation metric did you optimise and assess the model on? Why is this the most appropriate?_
- _Training: How did you arrive at the final set of hyperparameters? How did you manage imbalanced data or regularisation?_ -->
