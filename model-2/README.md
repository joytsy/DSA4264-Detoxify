# Model-2: Topic Modeling and Analysis

This folder contains resources and scripts for performing topic modeling and in-depth analysis of toxicity and hatefulness classification results. Using tools like BERTopic and hierarchical clustering, this module helps to extract meaningful topics from text data and analyze trends or intensity variations.

## Folder Structure

The `model-2` folder includes the following notebooks and directories:

1. **analysis.ipynb**

   - A comprehensive notebook for analyzing classification results. It provides visualizations and insights into the distribution of topics and classifications.

2. **bertopic.ipynb**

   - A notebook dedicated to using BERTopic for topic modeling. It details the steps to fit and transform text data, extract topics, and visualize topic distributions and relationships.

3. **experimenting_bertopic**

   - A folder containing experiments and additional scripts related to BERTopic. This may include testing different configurations, preprocessing methods, or parameters to optimize the topic modeling process.

4. **intensity_analysis.ipynb**

   - A notebook that analyzes the intensity of toxicity or hatefulness within identified topics. It includes techniques to measure how strongly a topic aligns with higher toxicity or hatefulness levels.

5. **redistribute\_-1.ipynb**
   - A script for redistributing or handling comments classified with a confidence score of -1, indicating uncertain classifications. It explores strategies to either reclassify or exclude such data points for better analysis.

---

## Usage

1. **Topic Modeling with BERTopic**:
   - Open `bertopic.ipynb` to perform topic modeling on your dataset. The notebook guides you through preprocessing text, fitting the BERTopic model, and visualizing the results.
2. **Experimenting with BERTopic**:
   - Explore the `experimenting_bertopic` folder for additional experiments and variations in BERTopic usage. Use these scripts to refine and optimize your topic modeling process.
3. **Analyzing Results**:
   - Use `analysis.ipynb` for a comprehensive analysis of the classification results. It includes various visualizations to understand topic distribution and relationships.
4. **Intensity Analysis**:
   - Open `intensity_analysis.ipynb` to measure and visualize the intensity of toxicity or hatefulness within topics. This analysis helps in understanding the severity of language used in different topics.
5. **Handling Uncertain Classifications**:
   - Use `redistribute_-1.ipynb` to manage data points with a classification confidence score of -1. This notebook suggests methods for redistributing or excluding such samples.

---

## Notes

- **BERTopic**: An advanced topic modeling technique that uses embeddings and clustering to identify coherent topics from text data. It is highly configurable and suitable for extracting meaningful insights from large text corpora.
- **Hierarchical Clustering**: Used alongside BERTopic to explore the relationships between identified topics and group similar ones for better interpretability.
- **Intensity Analysis**: Provides additional insights into the nature of toxicity or hatefulness within topics, helping to understand patterns and trends in the data.

---

Leverage the scripts in the `model-2` folder to perform advanced topic modeling and gain deeper insights into your classification results. Happy analyzing!
