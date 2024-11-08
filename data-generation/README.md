# Data-Generation Folder

This folder contains scripts and resources for generating synthetic data and labeling using both OpenAI's GPT-4o mini and Hugging Face models. The data generated here is used to address class imbalances and improve the performance of toxicity and hatefulness classifiers.

## Folder Structure

The `data-generation` folder is organized into three main subfolders: `huggingface`, `notebooks`, and `openai`. Additionally, there are standalone scripts to combine the synthetic datasets.

---

### 1. `huggingface` Folder

This folder contains scripts for labeling data using Hugging Face models. These scripts are used for both batch and single-sample labeling.

- **Files:**
  - **huggingface_batch.py**
    Script for labeling a batch of data using a Hugging Face model.
  - **huggingface.py**
    Script for labeling one data sample at a time using a Hugging Face model.

---

### 2. `notebooks` Folder

This folder contains Jupyter notebooks used for synthetic data generation. There are separate folders for each class:

1. **no_hate_toxic Folder:**

   - **no_hate_toxic.ipynb**: The first version of synthetic data generation.
   - **no_hate_toxic_final.ipynb**: The second version, with improvements over the first.
   - **no_hate_toxic_final_v2.ipynb**: The third version, with further enhancements.

2. **toxic_1 Folder:**

   - **toxic_1.ipynb**: The first version of synthetic data generation.
   - **toxic_1_final.ipynb**: The second version, with improvements over the first.
   - **toxic_1_final_v2.ipynb**: The third version, with further enhancements.

3. **toxic_2 Folder:**

   - **toxic_2.ipynb**: The first version of synthetic data generation.
   - **toxic_2_final.ipynb**: The second version, with improvements over the first.
   - **toxic_2_final_v2.ipynb**: The third version, with further enhancements.

4. **toxic_3 Folder:**

   - **toxic_3.ipynb**: The first version of synthetic data generation.
   - **toxic_3_final.ipynb**: The second version, with improvements over the first.
   - **toxic_3_final_v2.ipynb**: The third version, with further enhancements.

5. **hate_1 Folder:**

   - **hate_1.ipynb**: The first version of synthetic data generation.
   - **hate_1_final.ipynb**: The second version, with improvements over the first.
   - **hate_1_final_v2.ipynb**: The third version, with further enhancements.

6. **hate_2 Folder:**

   - **hate_2.ipynb**: The first version of synthetic data generation.
   - **hate_2_final.ipynb**: The second version, with improvements over the first.
   - **hate_2_final_v2.ipynb**: The third version, with further enhancements.

7. **hate_3 Folder:**
   - **hate_3.ipynb**: The first version of synthetic data generation.
   - **hate_3_final.ipynb**: The second version, with improvements over the first.
   - **hate_3_final_v2.ipynb**: The third version, with further enhancements.

Each version incorporates improvements and refinements in the data generation process to produce more realistic and balanced synthetic data.

---

### 3. `openai` Folder

This folder contains scripts for labeling data using OpenAI's GPT-4o mini. These scripts use both batch API requests and for-loop iterations for labeling.

- **Files:**
  - **openai_batch.ipynb**
    Notebook for labeling a batch of data using OpenAI's batch API.
  - **openai_generate_label.ipynb**
    Notebook for labeling data using a for loop, ideal for smaller datasets or when batch processing is not feasible.

---

## Additional Files

These files are used to combine synthetic data generated across different versions:

1. **data_combine.ipynb**
   Combines all synthetic data from the first version of each class.
2. **data_combine_final.ipynb**
   Combines all synthetic data from the second version of each class.
3. **data_combine_final_1million.ipynb**
   Combines all synthetic data from the third version, optimized for a larger dataset of up to 1 million samples.

---

## Usage

1. **Labeling Data with Hugging Face Models:**
   - Use `huggingface_batch.py` for batch labeling or `huggingface.py` for labeling one sample at a time.
2. **Generating Synthetic Data:**
   - Open the appropriate versioned notebook in the `notebooks` folder for the desired class (e.g., `hate_1_final_v2.ipynb` for the latest version).
3. **Labeling Data with OpenAI GPT-4o Mini:**
   - Use `openai_batch.ipynb` for batch processing or `openai_generate_label.ipynb` for labeling in a loop.
4. **Combining Synthetic Data:**
   - Use `data_combine.ipynb`, `data_combine_final.ipynb`, or `data_combine_final_1million.ipynb` to combine data from different versions as needed.

---

## Notes

- **Version Progression**: Each version of the synthetic data generation notebook improves upon the previous one, incorporating more sophisticated techniques and optimizations.
- **Data Combining**: The combination scripts ensure that synthetic data from different classes and versions are seamlessly merged for use in training models.

---
