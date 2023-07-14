# Yonei.dev fullstack blog

A Python application designed to serve as a feature rich personal blogging framework.

It parses Markdown files organized into numbered folders to generate an easy
navigable list of articles.  
Thanks to the power of [**FastAPI**][fastapi] and various [**Markdown addons**][1],
it simplifies the process of building and managing blogs.

This app also provides optional database integration for storing article views,
Prometheus metrics for monitoring, [**hot reloading**][2] for efficient
development and an interactive article listing thanks to the use of the
[**HTMX JavaScript framework**][htmx].

[1]: https://gitlab.com/yonei.dev/fullstack/-/blob/main/pyproject.toml#L19
[2]: https://github.com/florimondmanca/arel

# Features

- **Articles written in Markdown**: No need to store additional data in some database, backing up all the articles is as simple as moving a few files over.

- **Frontend Metadata**: Markdown files include frontend metadata, such as tags, titles, dates, authors and whatever else you'd like. This metadata allows users to categorize their articles, display informative titles, and sort content based on publishing dates.

- **Article Navigation:** The app generates a list of articles displayed on the home page, enabling seamless navigation for readers thanks to the use of [**HTMX**][htmx].

- **Database Integration**: The framework supports storing and retrieving article view metrics in a database. This feature allows users to track the popularity of their articles, the "view" is determined by a cookie session, no raw IP's in the database, no salts generated from various information, just an ssid stored in the cookie.

- **Prometheus Metrics**: Built-in integration with Prometheus enables users to monitor and expose various metrics. This includes monitoring server performance, request/response statistics, and other key indicators, providing valuable insights into the website's health and performance.

- **Hot Reloading**: The framework incorporates hot reloading, which means that changes made to Markdown files or the codebase are reflected in the running application. This accelerates blog writing, development and testing, allowing users to iterate quickly and efficiently.


# Quickstart
To get started with the blog app, follow the steps below:

1. Make sure you have `docker`, `docker-compose` and `git` installed *(optionally `python` and `poetry`)*

2. Clone this repository:
    ```sh
    git clone https://gitlab.com/yonei.dev/fullstack.git
    ```

3. Copy the `.env.example` file to `.env` and edit nescessary settings

4. Edit some Markdown files in the designated `posts` folder. Utilize the frontend metadata to enhance the user experience.

5. If you want to configure the database settings to store article view metrics. Refer to the provided [documentation][docs] for instructions on how to set up and connect to your database.

6. Build and run the app
    1. If you preffer `poetry`:
        ```sh
        poetry install
        poetry run python main.py
        ```
        *(**Note**: you can run `poetry run mkdocs build` to build the [documentation][docs])*
    
    2. If you preffer `docker`:
        ```sh
        docker compose up
        ```
        *(**Note**: add the `-d` flag to start in the background)*

7. Access the platform in your browser at `https://localhost:port`, the port being:
    - **If docker**: The port specified in the `docker-compose.yml` file (default external is 8080)
    - **If poetry**: The `APP_PORT` variable in the `.env` file

8. Pat yourself on the back and admire how great you are :3

For more detailed instructions and configuration options, please refer to the [documentation][docs].

# Contributing

Contributions are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features to the app, please open an issue or submit a pull request.

# License

The app is open-source and released under the [**MIT License**](LICENSE). You are free to use, modify, and distribute the framework in accordance with the terms of the license.

# Acknowledgements

We would like to express our gratitude to the [**FastAPI**][fastapi] community for providing an excellent web framework, [**PyMdown Extensions**](https://facelessuser.github.io/pymdown-extensions/) for great Markdown addons and the [**HTMX**][htmx] team for creating a wonderful JavaScript framework that isnt a pain in the ass to work with.

If you find this framework useful or have any feedback, we would love to hear from you! Please don't hesitate to reach out and share your thoughts.

[docs]: docs/
[fastapi]: https://fastapi.tiangolo.com/
[htmx]: https://htmx.org/
