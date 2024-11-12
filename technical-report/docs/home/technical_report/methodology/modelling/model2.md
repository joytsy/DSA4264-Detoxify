# Analyzing Reddit Data

## Overview

The objective of this analysis is to determine if, and why, the topics and comments on Reddit have become more hateful and toxic over recent years. To conduct this investigation, we employed a two-pronged analytical approach focusing on the frequency and intensity of toxic and hateful comments.

## Data Processing and Topic Modeling

The primary dataset utilized consisted of comments extracted from Reddit, with text data located in the `text` column of our DataFrame. We initiated our analysis by applying topic modeling technique using berTopic to categorize the comments into various topics.

### Text Preprocessing and Normalization

To address the linguistic characteristics of the Reddit dataset, which includes colloquial and region-specific language known as Singlish, we implemented a preprocessing routine tailored to convert Singlish terms into standard English. This preprocessing step involved the following actions:

1. **Dictionary Mapping**: A custom dictionary was developed to translate commonly used Singlish expressions to their English equivalents, which included removing expletives and colloquialisms that could skew the analysis. This dictionary also helped standardize different spellings of similar terms (e.g., “gahmen” and “gahment” both mapped to “government”).

2. **Text Normalization**: The text data was converted to lowercase to maintain consistency in processing. Special characters were removed to clean the text of any punctuation or extraneous symbols that do not contribute to semantic meaning.

3. **Stop Words Removal**: We integrated NLTK’s list of English stop words with additional custom stop words specific to our dataset to filter out noise and focus on meaningful words.

4. **Text Cleaning Function**: A text cleaning function was developed to automate the normalization process, which involved tokenization, dictionary-based term replacement, and stop word removal. This function was applied to each text entry in the dataset.

### Setting Up BERTopic for Topic Modeling

After preprocessing, we utilized BERTopic, an advanced topic modeling technique that leverages state-of-the-art language models and machine learning algorithms to discover topics within text data. The BERTopic setup involved several components designed to optimize topic extraction:

1. **Sentence Transformer**: The `SentenceTransformer` model, specifically `distiluse-base-multilingual-cased-v1`, was employed to generate dense vector representations of the cleaned text, capturing the contextual relationships between words.
2. **Dimensionality Reduction**: UMAP was configured to reduce the high-dimensional space of text embeddings into a lower-dimensional space that preserves the most important structural aspects of the data, facilitating more effective clustering.
3. **Clustering**: HDBSCAN was used to perform density-based clustering on the reduced embeddings, identifying groups of text with similar content without requiring a predetermined number of clusters.
4. **Representation Model**: A `KeyBERTInspired` representation model was implemented to select the most representative words for each topic based on their relevance and frequency, providing an interpretable summary of each topic.

During the topic modelling process, we identified a significant number of comments labeled with the topic identifier `-1`, indicating classification as outliers.

Upon further investigation of these outlier comments, we observed a that these comments were not assigned appropriate topics during the initial topic modeling phase even though the comments were relavant. To rectify this, we opted to reassess the `-1` labeled comments by extracting the Reddit thread topic from the `linkid` column rather than relying solely on the text content. This approach allowed us to understand the context surrounding the comments, which may lack explicit thematic elements yet still contribute to the overall discourse.

## Refinement of Topic Modeling

After re-evaluating the outlier comments, we integrated these findings with the previously identified topics into a unified dataframe. This integration process involved combining the refined `-1` topics with the existing topic classifications to ensure comprehensive coverage of the dataset.

Subsequently, we categorized these topics into twelve main themes for detailed analysis:

1. Body Image
2. COVID-19
3. Crimes
4. Education
5. Gender
6. Generational
7. Government
8. Housing
9. LGBTQ+
10. Religion
11. Transportation
12. Work

Utilizing the merging functionality provided by BERTopic, we consolidated related sub-topics into these main categories.

## Analysis of Topic Frequency and Intensity

Following the thematic categorization, we quantified the frequency of comments per topic to identify the most prevalent discussions. The frequency analysis aimed to pinpoint the topics that dominate the platform and assess their evolution over time in terms of both volume and intensity.

## Summary

This methodological approach, utilizing advanced topic modeling techniques and thematic analysis, serves to reveal insights into the shifting landscapes of discourse on Reddit. By examining the frequency and context of topics associated with toxic and hateful sentiments, we aim to uncover the underlying trends and catalysts contributing to the increase in such content on social media platforms.

- can explain more in depth for betopic
