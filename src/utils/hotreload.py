from src.core.logging import logger
from src.core.settings import settings

def initHotreload(app, templates):
    if not settings.HOTRELOAD:
        logger.warning(f"Hotreloading is disabled, HOTRELOAD={settings.HOTRELOAD}")
        return

    try:
        import arel
        from starlette.routing import WebSocketRoute

        hotreload = arel.HotReload([
            arel.Path("posts"),
            arel.Path("src/templates"),
            arel.Path("src/static/css")
        ])

        app.routes.append(WebSocketRoute("/hot-reload", hotreload, name="hot-reload"))
        app.on_startup.append(hotreload.startup)
        app.on_shutdown.append(hotreload.shutdown)
        templates.env.globals["ENABLE_HOTRELOAD"] = settings.HOTRELOAD
        templates.env.globals["hotreload"] = hotreload
    except ImportError:
        logger.exception("Arel could not be imported")
