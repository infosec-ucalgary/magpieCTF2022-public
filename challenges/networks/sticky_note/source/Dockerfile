FROM alpine:latest
RUN apk update && apk add openssh-server
RUN mkdir /var/run/sshd

RUN adduser -s /bin/sh -H -S papa # Add a user for ssh
RUN echo 'papa:keyissecret' | chpasswd # Assign a password to the user for ssh

# Prohibit someone to ssh as root
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN sed -i 's/AuthorizedKeysFile	.ssh\/authorized_keys/AuthorizedKeysFile \/authorized_keys/' /etc/ssh/sshd_config
COPY ./crazy_text.pub /authorized_keys

# SSH login fix. Otherwise user is kicked off after login
RUN /usr/bin/ssh-keygen -A
# RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Remove read and executable permissions for the user.
RUN chmod go-rx /usr/bin/passwd

RUN mkdir /papa
RUN mkdir /papa/bin /papa/lib

# sh shell
RUN cp /lib/ld-musl-x86_64.so.1 /papa/lib/
RUN cp /bin/sh /papa/bin/

# ls
RUN cp /bin/ls /papa/bin/

# cat
RUN cp /bin/cat /papa/bin/

WORKDIR /papa
RUN chown -R root:root /papa
RUN chmod -R 755 .
RUN chmod 1733 /tmp /var/tmp /dev/shm

#adding the flag to the docker container
COPY ./flag.txt /papa/flag.txt

# Configure default ssh shell as bash
# Define jailer as a recognised ssh user
RUN echo "Match User papa" >> /etc/ssh/sshd_config
# Define the chroot directory to be sshed into
RUN echo "  ChrootDirectory /papa" >> /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
