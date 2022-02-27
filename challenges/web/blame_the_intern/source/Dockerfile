FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /srv/app

ENV FLAG="magpie{tr34t_y0ur_1nt3rn5_n1c3ly}"

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py /srv/app

CMD ["python3", "app.py"]
