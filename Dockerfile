FROM python:3.10-alpine

WORKDIR /project

ARG ENVIRONMENT

# Copy pipenv files over
COPY Pipfile .
COPY Pipfile.lock .

# Generate requirements.txt and install dependencies
RUN apk add git
RUN pip install -U pipenv && \
    if [ "${ENVIRONMENT}" = "development" ]; then \
        pipenv requirements --dev > requirements.txt; \
    else \
        pipenv requirements > requirements.txt; \
    fi; \
    pip install --no-cache-dir -q -U -r requirements.txt

COPY app ./app
COPY posts ./posts

# If running behind a proxy add --proxy-headers and remove --reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
