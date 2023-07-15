# Introduction

This is a Python application designed to serve as a feature rich personal
blogging framework.

It parses Markdown files organized into numbered folders to generate an easy
navigable list of articles.  
Thanks to the power of [**FastAPI**][fastapi] and various [**Markdown addons**][1],
it simplifies the process of building and managing blogs.  
This app also provides optional database integration for storing article views,
[**Prometheus metrics**][3] for monitoring, [**hot reloading**][2] for efficient
development and an interactive article listing thanks to the use of the
[**HTMX JavaScript framework**][htmx].

[1]: https://gitlab.com/yonei.dev/fullstack/-/blob/main/pyproject.toml#L19
[2]: https://github.com/florimondmanca/arel
[3]: https://github.com/trallnag/prometheus-fastapi-instrumentator

[fastapi]: https://fastapi.tiangolo.com/
[htmx]: https://htmx.org/

## Where to start?

See the [Getting Started][1] section of the documentation or check the projects
`README.md` file.

To build the documentation run:

- If using `poetry`:
```sh
poetry run mkdocs build
```
- If using `docker`: MkDocs should be automatically built with the Docker
image, to rebuild the docs run:
```sh
docker compose build
```
or rebuild the docs in the running container:
```sh
docker exec container_name_or_id mkdocs build
```

[1]: getting_started/build_and_run_the_app/
