FROM python:3.9

RUN pip install pwntools;\
    pip install pycrypto;\
    pip install prometheus_client;\
    mkdir /monitor/

COPY solve.py /monitor/

CMD ["python3", "/monitor/solve.py"]
