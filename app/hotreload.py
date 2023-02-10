import arel

async def reload_data():
    print("Reloading server data...")

hotreload = arel.HotReload(
    paths=[
        arel.Path("posts", on_reload=[reload_data]),
        arel.Path("app/templates"),
    ],
)
