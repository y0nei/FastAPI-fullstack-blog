import markdown
from fastapi import HTTPException
from datetime import datetime
from app.schemas.sorting import SortChoices, OrderChoices

from pygments.formatters import HtmlFormatter
from markdown.extensions.codehilite import CodeHiliteExtension

class CustomHtmlFormatter(HtmlFormatter):
    def __init__(self, lang_str='', **options):
        super().__init__(**options)
        self.lang_str = lang_str

    def _wrap_code(self, source):
        yield 0, f'<code class="{self.lang_str}">'
        yield from source
        yield 0, '</code>'

def parseMarkdown(content: str) -> tuple[dict[str, str], str]:
    md = markdown.Markdown(extensions=['meta'])
    md.convert(content)

    # Split the markdown file into lines
    lines = content.split("\n")

    # Find the indices of the first two lines that contain separators
    separator_indices = [i for i, line in enumerate(lines) if line == "---"][:2]

    # If the first separator is on the first line of the file
    if separator_indices[0] == 0:
        # Remove the lines between the separators
        lines = lines[separator_indices[1] + 1:]

    # Join the remaining lines
    body = "\n".join(lines)

    return md.Meta, body

def convertMarkdown(content: str) -> str:
    return markdown.markdown(content, extensions=[
        'fenced_code',
        CodeHiliteExtension(pygments_formatter=CustomHtmlFormatter, css_class="highlight")
    ])

def getMetadata(post_id: int):
    try:
        with open(f"posts/{post_id}/content.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")

    metadata, _ = parseMarkdown(content)

    return {
        **metadata
    }

def sortPosts(arr: list, key: str | None = None, order=OrderChoices.ascending) -> list:
    if key is None:
        key = SortChoices.id
    elif not isinstance(key, SortChoices):
        raise ValueError(f"Invalid sort key '{key}', expected one of {list(SortChoices)}")

    reverse = order == OrderChoices.descending
    if key == SortChoices.date:
        sorted_arr = sorted(arr, key=lambda x: datetime.strptime(x[key][0], '%d-%m-%Y'), reverse=reverse)
    else:
        sorted_arr = sorted(arr, key=lambda x: x[key], reverse=reverse)

    return sorted_arr
