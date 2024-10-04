---
updated: 4 October 2024
authors:
  - Richmond Sin
---

# Formatting

## Frontmatter

Frontmatter is the "metadata" section of each markdown page. The following attributes must be present on all pages.

- `updated` -- date of which the page was last updated, in the DD-mmm-YYYY format.
- `authors` -- a string, or a list of strings matching the authors name(s) that contributed to the page.

These are required as the information is used to render the `updated` and `author` information at the bottom of the pages (hint: see the bottom of this page).

The following code block is an example of how to write the frontmatter at the very top of each markdown file.

    ---
    updated: 23 July 2024
    authors: Johnny Tan
    ---

## Hierarchy of Headers

Headers should reflect the logical hierarchy of the content. They must be used in sequential order, starting from H1 for the main title, then H2 for major subsections, followed by H3 for subtopics within those subsections, and so on. This structure is crucial as it helps in organizing the content clearly and logically, making it easier for readers to follow and understand the flow of information.
