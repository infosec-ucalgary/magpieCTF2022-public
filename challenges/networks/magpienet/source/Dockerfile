FROM ubuntu:latest

RUN apt update
RUN apt install -y python3-dev
WORKDIR /app
COPY . /app
RUN chmod u+x /app/run.sh
ENTRYPOINT ["bash", "/app/run.sh"]
