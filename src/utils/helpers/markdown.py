import markdown
from markdown.extensions.toc import TocExtension
from pymdownx.b64 import B64Extension

def parseMarkdown(content: str) -> tuple[dict[str, str], str]:
    md = markdown.Markdown(extensions=["meta"])
    md.convert(content)
    lines = content.split("\n")

    separator_indices = [i for i, line in enumerate(lines) if line == "---"][:2]
    if separator_indices[0] == 0:
        lines = lines[separator_indices[1] + 1:]

    body = "\n".join(lines)

    return md.Meta, body

def convertMarkdown(content: str) -> str:
    return markdown.markdown(content, extensions=[
        "tables",
        "sane_lists",
        "footnotes",
        TocExtension(permalink="#", toc_depth="1-3"),
        "markdown_checklist.extension",
        "markdown_del_ins",
        "markdown_sub_sup",
        "pymdownx.smartsymbols",
        "pymdownx.magiclink",
        "pymdownx.superfences",
        "pymdownx.highlight",
        B64Extension(base_path="posts")
    ])
