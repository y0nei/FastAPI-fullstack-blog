FROM python:3.10-alpine

WORKDIR /project

# Copy pipenv files over
COPY Pipfile .
COPY Pipfile.lock .

# Generate requirements.txt and install dependencies
RUN pip install pipenv && \
    pipenv requirements > requirements.txt && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY app ./app
COPY posts ./posts

# If running behind a proxy add --proxy-headers and remove --reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
