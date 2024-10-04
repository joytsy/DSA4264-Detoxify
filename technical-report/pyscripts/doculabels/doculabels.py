import re
from typing import Match

from mkdocs.structure.pages import Page

"""
Doculabels is a method for taking strings "@label(*)" and formatting them as html code blocks.
The intention for this is to improve readability of the documentation.

Supported label types:
- class
- pipe
- service
- interface
- type
- attr
- meth
- func
- private
- read only
"""


def __colour_factory(label: str) -> str:
    """
    Matches the label to a text colour variable.
    The variable is a CSS variable that ships with Material.
    :param label:
    :return:
    """

    colour_pairs = {
        "class": "var(--md-code-hl-constant-color)",
        "pipe": "var(--md-code-hl-constant-color)",
        "service": "var(--md-code-hl-constant-color)",
        "interface": "var(--md-code-hl-special-color)",
        "type": "var(--md-code-hl-special-color)",
        "attr": "var(--md-code-hl-number-color)",
        "meth": "var(--md-code-hl-color)",
        "func": "var(--md-code-hl-function-color)",
        "private": "var(--md-code-hl-string-color)",
        "read only": "var(--md-code-hl-string-color)",
        "default": "var(--md-code-fg-color)",
    }

    if label in colour_pairs.keys():
        return colour_pairs[label]
    else:
        print(label)
        return colour_pairs["default"]


def __replace_label(match: Match[str]) -> str:
    label_name = match.group(1).strip()
    label_colour = __colour_factory(label_name)

    return f"<code class='doculabel' style='color: {label_colour};'>{label_name}</code>"


def on_post_page(output: str, page: Page, config):
    pattern = r"@label\((.*?)\)"
    return re.sub(pattern, __replace_label, output)
