FROM python:3.9-alpine

# install make + gcc to ensure pycrypto can be installed
RUN apk add --update make;\
    apk add build-base;\
    pip3 install prometheus_client;\
    pip3 install requests;\
    pip3 install pycryptodome;\
    pip3 install pycrypto;\
    mkdir -p solve_server;

COPY linode-solve/files/server.py solve_server

CMD ["python3", "solve_server/server.py"]