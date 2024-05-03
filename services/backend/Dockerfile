FROM python:3.12

WORKDIR /usr/src

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install System Dependencies
RUN apt-get update \
    && apt-get -y install gcc postgresql \
    && apt-get clean \
    && pip install 'poetry'

# Install Python Dependencies
COPY ./services/backend/poetry.lock ./services/backend/pyproject.toml /usr/src/
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Add FastAPI App
COPY . .