import arel
from starlette.routing import WebSocketRoute
from app.settings import Settings

async def reload_data():
    print("Reloading server data...")

hotreload = arel.HotReload(
    paths=[
        arel.Path("posts", on_reload=[reload_data]),
        arel.Path("app/templates"),
    ],
)

def hotreloadSetup(app, templates):
    app.routes.append(WebSocketRoute("/hot-reload", hotreload, name="hot-reload"))
    app.router.on_startup.append(hotreload.startup)
    app.router.on_shutdown.append(hotreload.shutdown)
    templates.env.globals["DEBUG"] = Settings().DEBUG # Development flag.
    templates.env.globals["hotreload"] = hotreload
