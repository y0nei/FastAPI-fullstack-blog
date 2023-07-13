FROM python:3.11-slim AS build

RUN pip install --no-cache-dir -U poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export --with dev,markdown -f requirements.txt --output requirements.txt

FROM python:3.11-slim as setup

ENV PATH=$PATH:/home/docker/.local/bin \
    PYTHONUNBUFFERED=1

WORKDIR /project

RUN adduser --gecos "docker" docker
RUN chown -R docker:docker /project
RUN apt update
RUN apt install -y gcc git

USER docker
RUN git config --global --add safe.directory /project

COPY --from=build ./requirements.txt .
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U -r requirements.txt

COPY . .

RUN mkdocs build

ENTRYPOINT ["python3", "main.py"]
