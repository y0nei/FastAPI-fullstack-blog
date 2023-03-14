FROM python:3.11-alpine AS build

ARG ENVIRONMENT

RUN pip install -U pipenv
COPY Pipfile Pipfile.lock .

RUN if [ "${ENVIRONMENT}" = "development" ]; then \
        pipenv requirements --dev > requirements.txt; \
    else \
        pipenv requirements > requirements.txt; \
    fi

FROM python:3.11-alpine

ENV PATH=$PATH:/home/docker/.local/bin \
    PYTHONUNBUFFERED=1

WORKDIR /project

RUN apk add git

RUN adduser -D -g "docker" docker
RUN chown -R docker:docker /project
USER docker

COPY --from=build ./requirements.txt .
RUN pip install --no-cache-dir -U pip -r requirements.txt

COPY main.py .
COPY app ./app
COPY posts ./posts

ENTRYPOINT ["python3", "main.py"]
