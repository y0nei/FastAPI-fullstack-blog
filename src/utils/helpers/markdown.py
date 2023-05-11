import markdown
from pygments.formatters import HtmlFormatter
from markdown.extensions.codehilite import CodeHiliteExtension

class CustomHtmlFormatter(HtmlFormatter):
    def __init__(self, lang_str="", **options):
        super().__init__(**options)
        self.lang_str = lang_str

    def _wrap_code(self, source):
        yield 0, f"<code class=\"{self.lang_str}\">"
        yield from source
        yield 0, "</code>"

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
        "fenced_code",
        CodeHiliteExtension(pygments_formatter=CustomHtmlFormatter, css_class="highlight")
    ])
