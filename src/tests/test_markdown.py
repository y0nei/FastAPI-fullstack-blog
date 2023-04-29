import pytest
from src.helpers import parseMarkdown, convertMarkdown

with open("src/tests/samples/valid_markdown.md", "r") as f:
    valid_md = f.read()

expected_body = "\n".join([
    "This is the first paragraph of the document.",
    "",
    "# This is a heading",
    "---",
    "",
    "and **here** is a [Link](#) and `inline code`",
    ""  # <-- Extra new line since i code in vim lol
])

expected_metadata = {
    'title': ['My Document'],
    'description': ['A brief description of my document.'],
    'authors': ['Waylan Limberg', 'John Doe'],
    'date': ['October 2, 2007'],
    'blank-value': [''],
}

def test_parseMarkdown_body_and_metadata_separation():
    """
    Compares metadata and body to the expected strings above
    """
    metadata, body = parseMarkdown(valid_md)
    assert metadata == expected_metadata
    assert body == expected_body

def test_parseMarkdown_invalid_frontmatter():
    """
    Checks if asserting 'metadata' returns an error and if the list is empty.
    Checks if the whole markdown body gets returned, when no metadata is read.
    """
    with open("src/tests/samples/invalid_frontmatter.md", "r") as f:
        invalid_frontmatter_md = f.read()
    metadata, body = parseMarkdown(invalid_frontmatter_md)
    with pytest.raises(AssertionError):
        assert metadata == expected_metadata
    assert metadata == {}
    assert body == invalid_frontmatter_md

def test_convertMarkdown():
    """
    Checks if the convertMarkdown function properly converts markdown to html
    """
    with open("src/tests/samples/valid_markdown.html", "r") as f:
        expected_html = f.read()
    result = convertMarkdown(expected_body)
    assert result + "\n" == expected_html

def test_convertMarkdown_codeblocks():
    """
    Checks if the convertMarkdown function properly converts markdown codeblocks
    with CodeHilite syntax highlighting to html
    """
    with open("src/tests/samples/codeblocks.md", "r") as f:
        sample_codeblock_md = f.read()
    with open("src/tests/samples/codeblocks.html", "r") as f:
        expected_codeblock_html = f.read()
    result = convertMarkdown(sample_codeblock_md)
    assert result + "\n" == expected_codeblock_html
