import arel
from fastapi.templating import Jinja2Templates
from src.core.settings import settings
from src.utils.sass import compile_sass

hotreload = arel.HotReload([
    arel.Path("posts"),
    arel.Path("src/templates"),
    arel.Path("src/static/scss", on_reload=[compile_sass])
])

def initHotreload(templates: Jinja2Templates) -> None:
    templates.env.globals["ENABLE_HOTRELOAD"] = settings.HOTRELOAD
    if settings.HOTRELOAD:
        templates.env.globals["hotreload"] = hotreload
