from app.settings import settings, logger

async def reload_data():
    logger.info("Reloading server data...")

def initHotreload(app, templates):
    if settings.DEBUG != 1 or settings.ENVIRONMENT != "development":
        logger.warning("Hotreloading is disabled")
        return

    try:
        import arel
        from starlette.routing import WebSocketRoute

        hotreload = arel.HotReload([
            arel.Path("posts", on_reload=[reload_data]),
            arel.Path("app/templates"),
            arel.Path("app/static/css")
        ])

        app.routes.append(WebSocketRoute("/hot-reload", hotreload, name="hot-reload"))
        app.on_startup.append(hotreload.startup)
        app.on_shutdown.append(hotreload.shutdown)

        templates.env.globals["DEBUG"] = settings.DEBUG
        templates.env.globals["hotreload"] = hotreload
    except ImportError:
        logger.exception("Arel could not be imported")
