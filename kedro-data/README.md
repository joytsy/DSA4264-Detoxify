# kedro_data

## Overview

This is your new Kedro project with Kedro-Viz setup, which was generated using `kedro 0.19.8`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines

In order to get the best out of the template:

- Don't remove any lines from the `.gitignore` file we provide
- Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
- Don't commit data to your repository
- Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```python
pip install -r requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```python
kedro run
```

You can run your Kedro project specific pipeline with:

```python
kedro run --pipeline="data_processing"
```

You can run your Kedro project specific node with:

```python
kedro run --nodes=”remove_deleted_comments_node”
```

## How to test your Kedro project

Have a look at the files `src/tests/test_run.py` and `src/tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```python
pytest
```

To configure the coverage threshold, look at the `.coveragerc` file.