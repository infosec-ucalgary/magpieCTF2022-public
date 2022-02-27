FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

# Install dependencies.
RUN pip install --no-cache-dir python-dotenv requests

# Copy app.
COPY ./app /app

EXPOSE 80