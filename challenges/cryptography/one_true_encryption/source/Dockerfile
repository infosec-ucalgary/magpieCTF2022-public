FROM ubuntu:20.04

RUN apt update
RUN apt install -y python3 socat python3-pip libldap2-dev libsasl2-dev
RUN python3 -m pip install --upgrade pyOpenSSL
RUN python3 -m pip install --upgrade pycrypto secrets

COPY *.py /home/
COPY ntru/*.py /home/

EXPOSE 31337

CMD socat TCP-LISTEN:31337,fork,reuseaddr EXEC:"python3 /home/channel.py"
