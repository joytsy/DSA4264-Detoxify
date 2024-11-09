# Scope

## 1. Problem

### 1.1 Problem Faced by MDDI

The Online Trust and Safety Department is tasked with safeguarding the digital space for Singaporean users, particularly children and vulnerable groups. However, the team currently lacks concrete data on the scale and evolution of hate and toxic behaviour on Singapore-focused subreddits. Without a detailed, historical analysis of trends in online toxicity, it is challenging for MDDI to understand the extent of the issue or to identify the specific factors driving increased hatefulness and toxicity. This lack of data impedes the department’s ability to design targeted interventions and effectively engage with social media platforms to mitigate risks.

### 1.2 Significance of the Problem

The rise in online hatefulness and toxicity poses significant social risks, particularly for a diverse society like Singapore, where online discourse can influence public sentiment and community relations. The Online Safety Poll indicates an upward trend in harmful content exposure, with potential consequences for youth and societal cohesion. Not addressing this problem could lead to increased polarisation, a diminished sense of safety in online spaces, and potentially a negative impact on public trust. Metrics include the reported increase in harmful content exposure (from 57% to 66% of users within a year), with particular focus on high-risk age groups and vulnerable populations.

### 1.3 Why a Data Science Approach is Essential

Given the massive volume of data and the nuances of language, manual review is impractical for identifying trends in online hate and toxicity across the years. Data science enables scalable, data-driven analysis, and leveraging Natural Language Processing (NLP) techniques helps MDDI to automate the detection and classification of hate and toxic comments, enabling the extraction of actionable insights at scale. By analyzing comment-level data over time, MDDI can gain insights into the extent of the issue, providing them with an efficient means of tracking trends over time and identifying themes associated with heightened hatefulness and toxicity on social media.

## 2. Success Criteria

Should this project be successful, the following business and operational goals will be met:

**Insightful Reporting for Policy Development:** Generate clear, data-backed insights on hate and toxic speech in the online environment, by observing trends over the recent years (2020 to 2023) and the specific factors and subjects involved. These meaningful insights will be able to support MDDI in their policy recommendations and interventions to curb the problem in a precise manner. MDDI can then implement actionable strategies, including the engagement of various stakeholders like social media companies, to aid in reducing the exposure of such of these harmful content.

**Automated Hatefulness/Toxicity Detection Pipeline:** Develop a reliable pipeline that automates the processing and classification of Reddit comments by hatefulness or toxicity levels. This automation will be able to read in a Reddit comment, before classifying it into one of the 7 categories under the [Language Intensity Classification](./methodology/index.md) system defined by us. This system will increase MDDI’s capacity to monitor and analyse social media content efficiently, with minimal manual intervention. In addition, with the classification of comments into the 7 categories, MDDI can better understand the change in intensity of online hate/toxicity trends over the years, the causes driving these trends and ultimately implement targeted solutions.

**Enhanced Public Trust and Safety:** After the completion of detailed data-driven analysis, tailored strategies and recommendations can be provided to social media companies to create a safer digital environment, particularly for youths. Success in this goal will be measured by increased collaboration between MDDI and social media platforms on reducing harmful content on Singapore-focused subreddits.

## 3. Assumptions

**Availability of Sufficient Historical Data:** The project assumes that the provided Reddit comment data will be sufficient in volume and time span (2020 to 2023) to detect meaningful trends in online toxicity. If data gaps or limitations arise, the scope and depth of trend analyses may be affected.

**Accuracy of NLP Models in Capturing Nuanced Toxicity:** The analysis assumes that NLP models used for hate speech and toxicity detection can accurately capture nuanced and context-specific language that may be uniquely reflective of the Singaporean context. Inaccuracies or model limitations could affect the reliability of toxicity assessments.

**Engagement from Social Media Platforms:** The project’s success partially depends on the willingness of social media companies to consider and act upon MDDI’s findings and recommendations. Limited cooperation from these stakeholders could reduce the overall impact of policy recommendations derived from the project.
