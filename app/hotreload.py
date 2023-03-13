from app.settings import settings

async def reload_data():
    print("Reloading server data...")

def initHotreload(app, templates):
    if settings.DEBUG != 1 or settings.ENVIRONMENT != "development":
        print(">To enable browser hotreloading: set DEBUG to 1",
              "\n>and ENVIRONMENT to development in the .env file")
        return

    try:
        import arel
        from starlette.routing import WebSocketRoute

        hotreload = arel.HotReload(
            paths=[
                arel.Path("posts", on_reload=[reload_data]),
                arel.Path("app/templates"),
            ],
        )

        # TODO: Read Arel reload dirs to settings
        app.routes.append(WebSocketRoute("/hot-reload", hotreload, name="hot-reload"))
        app.on_startup.append(hotreload.startup)
        app.on_shutdown.append(hotreload.shutdown)

        templates.env.globals["DEBUG"] = settings.DEBUG
        templates.env.globals["hotreload"] = hotreload

    except ImportError:
        print(">Arel could not be successfully imported",
              "\n>Make sure your docker build args match the environment")
