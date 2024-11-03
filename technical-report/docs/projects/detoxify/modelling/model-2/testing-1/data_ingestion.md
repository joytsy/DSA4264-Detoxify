---
updated: 4 October 2024
authors:
  - Richmond Sin
---

# Data Ingestion

The ingestion process involves bringing HealthHub articles (in JSON format) into the system, processing them through Azure services, and storing them in an Azure Search Index for querying.

The ingestion process begins by uploading the JSON files containing article data to **Azure Blob Storage**. Blob Storage acts as a scalable storage solution that can hold a large number of documents and media files. Each document represents a single article with fields like id, title, content_category, content, etc. The typical structure of these JSON files includes fields like:

- **id**: A unique identifier for the article.
- **title**: The title of the article.
- **cover_image_url**: A URL pointing to an image associated with the article.
- **full_url**: A URL to the article’s full content on HealthHub.
- **content_category**: The category under which the article falls (e.g., 'programs').
- **category_description**: The description of the article at the top of the page.
- **pr_name**: The name of the article provider.
- **date_modified**: The last edited date of this article (if any).
- **content**: The body of the article itself.

## JSON Example

```json
[
  {
    "id": "1434570_content",
    "title": "National Steps Challenge™ Community Challenge",
    "cover_image_url": "https://github.com/",
    "full_url": "https://github.com/",
    "content_category": "programs",
    "category_description": "Feel good with every move as you bond with your neighbours! The National Steps Challenge™ Season 5 is back with Community Challenge!",
    "pr_name": "Health Promotion Board",
    "date_modified": "2024-09-10",
    "content": "your content here"
  }
]
```

## Steps for Data Ingestion

1. **Uploading to Blob Storage**: The JSON files are uploaded to Azure Blob Storage to persist and stage the data before indexing.

2. **Inserting Documents into the Azure Search Index**: Once uploaded, the documents are inserted into the Azure Search Index using the `SearchClient`. The document fields are mapped to the corresponding index fields, enabling full-text search, filtering, sorting, and faceting functionalities. The primary client types used in the process are:

   - **SearchClient**: Handles individual document operations such as adding or deleting documents from the search index.
   - **SearchIndexClient**: Used for managing the index itself, including creating, updating, or deleting indexes.
   - **SearchIndexerClient**: Manages automated indexing pipelines, integrating Blob Storage or databases as data sources.

3. **Chunking and Embedding**: This pipeline handles the ingestion of articles into the search index. It consists of two major skills:

   - **SplitSkill (Chunking)**: Splits the article content into manageable chunks.
   - **Azure OpenAI EmbeddingSkill**: Generates embeddings for each chunk, using the model `text-embedding-3-small`.

4. **Search Index Creation**: After chunking and embedding, the data is stored in the Azure Search Index for retrieval. The search index is configured to allow full-text and vector search.
