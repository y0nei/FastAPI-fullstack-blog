from app.settings import settings

async def reload_data():
    print("Reloading server data...")

def initHotreload(app):
    if settings.DEBUG != 1 or settings.ENVIROMENT != "development":
        print(">To enable browser hotreloading: set DEBUG to 1",
              "\n>and ENVIROMENT to development in the .env file")
        return

    try:
        import arel

        # TODO: Read Arel reload dirs to settings
        app.add_middleware(arel.HotReloadMiddleware, paths=[
            arel.Path("posts", on_reload=[reload_data]),
            arel.Path("app/templates")
        ])
    except ImportError:
        print(">Arel could not be successfully imported",
              "\n>Make sure your docker build args match the enviroment")
