# Use the official Python 3.11 image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies for Poetry
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential libpq-dev && \
  rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip3 install poetry

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

COPY . /app

# Install the dependencies using Poetry
RUN poetry install 

ARG GYTDL_API_KEY

# Expose the port FastAPI will run on
EXPOSE 8000

# Run Gunicorn with Uvicorn workers
CMD ["poetry","run","gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000"]
