FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /srv/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py /srv/app
COPY static /srv/app/static
COPY templates /srv/app/templates

CMD ["python3", "app.py"]