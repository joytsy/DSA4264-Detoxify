# Model-2: Topic Modeling and Analysis

This folder contains resources and scripts for performing topic modeling and in-depth analysis of toxicity and hatefulness classification results. Using tools like BERTopic and hierarchical clustering, this module helps to extract meaningful topics from text data and analyze trends and intensity variations.

## Folder Structure

The `model-2` folder includes the following notebooks and directories:

1. **frequency_analysis.ipynb**

   - A comprehensive notebook for analyzing classification results, providing visualizations and insights into topic and classification distributions.

2. **bertopic.ipynb**

   - A notebook dedicated to using BERTopic for topic modeling. It details the steps to fit and transform text data, extract topics, and visualize topic distributions and relationships.

3. **intensity_analysis.ipynb**

   - A notebook for the overview of the intensity of toxicity or hatefulness of the identified topics.

4. **redistribute\_-1.ipynb**

   - A script for redistributing comments initially classified as outliers (-1) by applying topic modeling to Reddit titles. It aims to improve the categorization of comments that previously did not fit into established topics.

5. **intensity_trend_analysis.ipynb**

   - A notebook that analyzes the intensity trends of topics. It includes visualisation tools such as graphs and word clouds to garner insights into specific topics.

6. **solutions.ipynb**

   - A notebook that generates a problem statement based on the DataFrame of comments inputted.

---

## Usage

1. **Topic Modeling with BERTopic**:

   - Open `bertopic.ipynb` to perform topic modeling on your dataset. The notebook guides you through preprocessing text, fitting the BERTopic model, and visualizing the results.

2. **Redistribution of Outlier Topic Comments**:
   -Use `redistribute_-1.ipynb` to apply topic modeling techniques on Reddit titles to categorize and redistribute outlier comments effectively.

3. **Intensity Overview of Topics**:

   - Use `intensity analysis.ipynb` for a intensity overview of the various topics.

4. **Analyzing Topic Frequency**:

   - Open `frequency_analysis.ipynb` to analyze topic distribution and comment frequency. Visualize how topics are distributed and how intensity levels (hate or toxicity) relate to specific topics.

5. **Analyzing Intensity Trends**:

   - Use `intensity_trend_analysis.ipynb` to measure the intensity of toxicity and hatefulness within topics. This notebook helps visualize the severity of language over time and within specific topics.

6. **Generating Problem Statements**:
   - Open `solutions.ipynb` to generate problem statements based on your filtered and sequenced comments. It uses OpenAI to create problem statements directly from the insights you’ve gathered

---

## Notes

- **BERTopic**: An advanced topic modeling technique that uses embeddings and clustering to identify coherent topics from text data. It is highly configurable and suitable for extracting meaningful insights from large text corpora.
- **Hierarchical Clustering**: Used alongside BERTopic to explore the relationships between identified topics and group similar ones for better interpretability.
- **Intensity Trend Analysis**: Provides additional insights into the nature of toxicity or hatefulness within topics, helping to understand patterns and trends in the data.

---

Leverage the scripts in the `model-2` folder to perform advanced topic modeling and gain deeper insights into your classification results. Happy analyzing!
