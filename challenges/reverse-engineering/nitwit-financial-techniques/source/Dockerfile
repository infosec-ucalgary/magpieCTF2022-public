FROM python:alpine3.15

# install cron and vim
RUN apk update; apk upgrade;

# set working directory as /app
WORKDIR /app

# copy the crontab into cron.d
COPY crontab /etc/cron.d/crontab

# copy the python program
COPY ./email-checker/* /app/

# chmod the new crontab
RUN chmod 0644 /etc/cron.d/crontab

# run crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD crond -l 0 -f