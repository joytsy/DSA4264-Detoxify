# Documentation Guides

To ensure consistency in our documentation, the guides in this folder are intended to set a standard for documentation practices.
As there are various types of documentation subjects, such as processes, classes, and interfaces; this is a general guide on how to document them effectively.

---

## Objectives for Documentation

Documentation should be concise and focused on providing a knowledge base for quick reference, enabling contributors to understand the codebase without needing to deeply dive into the code. Documentation should be kept up to date with the latest changes, therefore they should be updated in tandem with code development.

---

## Formatting

### Front Matter

All document files should start with front matter that includes (minimally) the following attributes.

1. Updated (date of last update), in `DD MMM YYYY` format.
2. Author, an array of names.

> [!TIP]
>
> ```text
> ---
> updated: 19 July 2024
> author: [James Teo, John Tan]
> ---
> ```

### Classes, Types, etc

An additional `JavaScript` is attached to MkDocs when serving. This file (`doculabels.js`) is responsible for allowing us to label classes, types, interfaces etc. in colour-coded code blocks that will be seen in the browser.

In the markdown files for MkDocs, we can use the following annotation styling in headers.

```text
@label(...)
```

Supported labels

1. `class`
2. `service`
3. `interface`
4. `pipe`
5. `type`
6. `func`
7. `meth`
8. `attr`

> [!TIP]
> This must be used in a header block
>
> ```text
> ## @label(class) MyDocumentedClass
> ```
