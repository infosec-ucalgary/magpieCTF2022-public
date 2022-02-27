FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

# Install dependencies.
RUN pip install --no-cache-dir python-dotenv

# Copy app.
COPY ./server/app /app

# Add entry for handler to supervisord.
COPY ./server/supervisord-handler.ini /etc/supervisor.d/supervisord-handler.ini

EXPOSE 80
