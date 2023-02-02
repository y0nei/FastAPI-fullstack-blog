import markdown
from fastapi import HTTPException

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

def getMetadata(post_id: int):
    try:
        with open(f"posts/{post_id}/content.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")

    # Extract the front matter from the markdown file
    metadata, _ = parseMarkdown(content)

    return {
        "id": post_id,
        **metadata
    }
