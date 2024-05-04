FROM python:3.12-slim-bookworm

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy a simulated secret file to test your future kubernetes secret deployment
COPY appconfig.conf /app/secrets/appconfig.conf

WORKDIR /app
COPY . /app

# Creates a non-root user and adds permission to access the /app folder
RUN useradd appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["uvicorn","app.main:app","--port","8000","--host","0.0.0.0"]
