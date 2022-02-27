FROM ubuntu

ENV FLAG="magpie{0u7_0f_\$1gh7;)}"

ENV DEBIAN_FRONTEND noninteractive

RUN apt update -y && \
      apt upgrade -y &&\
      apt-get install finger fingerd inetutils-inetd openssh-server sshpass -y &&\
      useradd --shell /bin/sh --home-dir /home/myUser -g root myUser&&\
# /etc/init.d/inetutils-inetd restart &&\
      echo 'myUser:zkUTe9V$hZwTU&!w' | chpasswd &&\
      mkdir -p /home/myUser/.ssh &&\
      echo '<PUBLIC KEY>' >> /home/myUser/.ssh/authorized_keys &&\
      chown myUser:root /home/myUser/.ssh/authorized_keys &&\
      chfn -f $FLAG myUser

COPY inetd.conf /etc/inetd.conf
COPY start_service.sh start_service.sh
ENV DEBIAN_FRONTEND text

# RUN /etc/init.d/ssh start

CMD ["./start_service.sh"]

# older attempts to get this running autonomously

# CMD ["sshpass", "-p", "zkUTe9V$hZwTU&!w" ,"ssh", "myUser@127.0.0.1"]
# CMD ["echo", "/etc/init.d/ssh", "start", "|", "/bin/bash", "-i"]
# RUN /etc/init.d/ssh restart
# RUN /etc/init.d/inetutils-inetd restart
# CMD ["python3", "-m", "http.server"]
# CMD ["/etc/init.d/ssh", "start", "-D"]
