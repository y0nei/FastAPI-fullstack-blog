from fastapi.templating import Jinja2Templates
from src.utils.helpers.version import get_git_version, get_git_url_and_branch
from src.utils.hotreload import initHotreload

templates = Jinja2Templates(
    directory="src/templates",
    # Whitespace control
    lstrip_blocks=True,
    trim_blocks=True
)

templates.env.globals["git_version"] = get_git_version()
templates.env.globals["git_url"] = get_git_url_and_branch().get("url")
initHotreload(templates)
