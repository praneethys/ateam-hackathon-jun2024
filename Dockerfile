FROM python:3.11 as build

# Set the working directory to /app
WORKDIR /app

ENV PYTHONPATH=/app

# Install any needed packages specified in requirements.txt
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip pip install poetry

RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install

# Download the 'stopwords' resource before running the app
RUN python -c "import nltk; nltk.download('stopwords')"
# RUN chmod -R 775 /usr/local/lib/python3.11/site-packages/llama_index

# ====================================
FROM build as release

COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

ENV POSTGRES_USER codepath_project_owner
ENV POSTGRES_PASSWORD 03EdiworgCJz
ENV POSTGRES_DB_NAME codepath_project
ENV POSTGRES_DB_HOST ep-icy-cloud-a5m4mcgo.us-east-2.aws.neon.tech
ENV POSTGRES_DB_PORT 5432

# Run migrations
RUN alembic upgrade head

CMD ["python", "main.py"]
