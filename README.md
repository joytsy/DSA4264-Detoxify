# DSA4264-Detoxify

## Overview

This project is part of DSA4264, focusing on the use of Detoxify for analyzing toxic comments. The following setup instructions will help you get started with the project. Ensure that the dependencies are properly installed, and the data pipeline is configured correctly.

## Rules and Guidelines

- **Do not remove any lines from the `.gitignore` file** provided in the repository to prevent committing unnecessary or sensitive files.
- **Do not commit any data or credentials** to the repository. Keep all credentials and configurations in `conf/local/` or secure external storage.

## How to Set Up the Project

1. **Create a Virtual Environment** (Ensure that you are using **Python 3.12**)

   Windows:

   ```bash
   md penv
   cd penv
   python -m venv .
   Scripts\activate  # To activate the virtual environment
   deactivate  # To deactivate the environment
   ```

   Mac:

   ```bash
   mkdir penv
   cd penv
   python3.12 -m venv .
   source bin/activate  # To activate the virtual environment
   deactivate  # To deactivate the environment
   ```

2. **Install Dependencies**

   To install the required dependencies, run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Pre-Commit Hooks**

   To maintain code quality, set up the pre-commit hooks by running:

   ```bash
   pre-commit install
   ```

4. **Navigate to the Data Directory**

   Change into the `kedro-data` directory to configure and manage the data processing pipeline:

   ```bash
   cd kedro-data
   ```

5. **Configure the Data Pipeline**

   After navigating to the kedro-data directory, follow the instructions provided there to set up and run the data processing pipeline.
