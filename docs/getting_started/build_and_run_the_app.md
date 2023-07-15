In order to build and run the app, refer to the projects `README.md` file
or follow the steps below:

1. Make sure you have `docker`, `docker-compose` and `git` installed and
   configured on your system *(optionally `python` and `poetry`)*

2. Clone the repository
    ```sh
    git clone https://gitlab.com/yonei.dev/fullstack.git
    ```

3. Copy the `.env.example` file to `.env` and edit nescessary settings[^1]

4. Build and run the app
    1. If you preffer `poetry`:
        ```sh
        poetry install
        poetry run python main.py
        ```

    2. If you preffer `docker`:
        ```sh
        docker compose up
        ```
        *(**Note**: add the `-d` flag to start in the background)*

5. Access the platform in your browser at `localhost:port`, the port being:
    - **If docker**: The port specified in the `docker-compose.yml` file (default external is 8080)
    - **If poetry**: The `APP_PORT` variable in the `.env`[^1] file (default is 8000)

[^1]: [environment variable documentation](../configure_the_environment)
