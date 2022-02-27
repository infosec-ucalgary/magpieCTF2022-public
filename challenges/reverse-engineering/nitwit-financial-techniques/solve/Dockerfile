FROM python:alpine3.15

# install cron and vim
RUN apk update; apk upgrade; pip3 install prometheus-client

# set working directory as /app
WORKDIR /app

# copy the crontab into cron.d
#COPY crontab /etc/cron.d/crontab

# copy the python program
COPY solve.py /app/

# copy the fingerprint png file
COPY fingerprint.png /app/

# chmod the new crontab
#RUN chmod 0644 /etc/cron.d/crontab

# run crontab
#RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD python /app/solve.py