FROM python:3.11-alpine AS build

RUN pip install --no-cache-dir -U poetry

COPY pyproject.toml poetry.lock ./
RUN poetry export --with dev -f requirements.txt --output requirements.txt

FROM python:3.11-alpine

ENV PATH=$PATH:/home/docker/.local/bin \
    PYTHONUNBUFFERED=1

WORKDIR /project

RUN adduser -D -g "docker" docker
RUN chown -R docker:docker /project
USER docker

COPY --from=build ./requirements.txt .
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U -r requirements.txt

COPY main.py .
COPY src ./src
COPY posts ./posts

ENTRYPOINT ["python3", "main.py"]
