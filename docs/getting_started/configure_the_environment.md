The default `.env` file contains the following settings:

```py title=".env.example"
APP_NAME="Awesome blog"
LOG_LEVEL=info
POST_STATISTICS=0
HOTRELOAD=1
ENABLE_METRICS=1
ENVIRONMENT=development
APP_HOST=0.0.0.0
APP_PORT=8000

# Secret key | to generate, use something like "openssl rand -base64 32"
SECRET_KEY=randomstring

# Database variables
DB_USER=user
DB_PASSWORD=password
DB_HOST=0.0.0.0
DB_PORT=27017
DB_NAME=database
```

## Setting descriptions:
For a list of default values refer to the `settings.py` file.[^2]

- `APP_NAME`: A string used to determine the name of your site, will be
  displayed as the FastAPI app title, websites head `<title>` element,
  OpenAPI Specification & ReDoc app documentation title.

- `LOG_LEVEL`: Controls the log level of the Uvicorn server[^1].
    - **Options**: critical, error, warning, info, debug, trace.

- `POST_STATISTICS`: If set to `true` or `1` do a few things:
    - expose various database-related settings to the app[^2]
    - enable the database functionality for view storage
    - control if [starlettes session middleware][1] should be initialized
    - and if the cookie consent banner should be shown or not

- `HOTRELOAD`: If set to `true` or `1`, enable the hot reloading functionality.
  Your browser should be automatically reloaded when a change is detected in
  the paths defined in the `/src/utils/hotreload.py` file.
    - By default, all changes to Html templates, Markdown files and Scss styles
      trigger a reload

- `ENABLE_METRICS`: If set to `true` or `1`, expose the Prometheus
  instrumentator. You should see data appear on the `/metrics` route

- `ENVIRONMENT`: If set to `"development"`, allows the app to re-compile Scss
  files on startup and enables the Uvicorn `reload` option.[^3]
    - Available options are either "production" or "development"[^2]

- `APP_HOST`: Define the host to start the Uvicorn server on, by default its
  just localhost.

- `APP_PORT`: Define the **internal** port the Uvicorn server will run on.
    - **Note**: If running in docker, the internal port is on the right side,
    while the external port (port you will access the app from) is on the left.
    ```yaml hl_lines="2" title="docker-compose.yml"
    ports:
      - "external_port:internal:port"
    ```
- `SECRET_KEY`: Used for [starlettes session middleware][1] cookie signing, as
  the docs state, it "Should be a random string."

### Database settings
- Variables used in the MongoDB connection string[^2]:
    - `DB_USER`: MongoDB username.
    - `DB_PASSWORD`: MongoDB password.
    - `DB_HOST`: Database URL.
    - `DB_PORT`: The database port.

- `DB_NAME`: The database which to use to create the view collection in.

[1]: https://www.starlette.io/middleware/#sessionmiddleware

[^1]: See [Uvicorn logging docs](https://www.uvicorn.org/settings/#logging)
[^2]: See the `/src/core/settings.py` file
[^3]: See [Uvicorn settings](https://www.uvicorn.org/settings/#development)
