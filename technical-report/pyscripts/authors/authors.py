from typing import Dict, List, Union

from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

"""
This file is responsible for setting page meta attributes for author details.

1. MD file must have a "authors" attribute in the front header. It can be a list of strings, or a single string.
This must match either the full name of "extra.authors" in mkdocs.yml, or match "extra.authors.[name].alias".

mkdocs.Authors = List[{
    [key:string]: {
        alias: string | List[string],
        role: string,
        avatar: string,
        url: string
    }
}]

2. To set the authors information for rendering, "page.meta['_authors']" is set with the following schema.

List[{
    name: string,
    role: string,
    avatar: string,
    url: string,
}]

"""


def __getPageAuthors(
    names: Union[str, List[str]], all_authors: List[Dict[str, any]]
) -> List[Dict[str, str]]:
    """
    Function to
    :param names: Names (or aliases) of authors that have been stated in the markdown file.
    :param all_authors: Authors defined in mkdocs.yml
    :return: Authors schema (see comment above)
    """

    authors = []

    ### Handle single string
    if isinstance(names, str):
        names = [names]

    for name in names:
        for a in all_authors:
            current_author_name = list(a.keys())[0]
            current_author = a[current_author_name]

            # Convert single entry alias into an array
            if isinstance(current_author["alias"], str):
                current_author["alias"] = [current_author["alias"]]

            if name == current_author_name or name in current_author["alias"]:
                authors.append(
                    {
                        "name": current_author_name,
                        "role": current_author["role"],
                        "avatar": current_author["avatar"],
                        "url": current_author["url"],
                    }
                )

    return authors


def on_page_context(context: TemplateContext, page: Page, config: Dict[str, any], nav):
    if "authors" in page.meta.keys():
        page.meta["_authors"] = __getPageAuthors(
            page.meta["authors"], config["extra"]["authors"]
        )
    return context
