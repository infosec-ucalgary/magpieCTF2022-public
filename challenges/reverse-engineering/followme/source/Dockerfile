FROM archlinux:base-devel
RUN pacman -Sy --noconfirm vim openssh strace
RUN mkdir /var/run/sshd

RUN useradd -m magpie # Add a user for ssh
RUN echo 'magpie:keyissecret' | chpasswd # Assign a password to the user for ssh

# Prohibit someone to ssh as root
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN sed -i 's/AuthorizedKeysFile    .ssh\/authorized_keys/AuthorizedKeysFile \/authorized_keys/' /etc/ssh/sshd_config
COPY ./app/followme_rsa.pub /authorized_keys

# SSH login fix. Otherwise user is kicked off after login
RUN /usr/bin/ssh-keygen -A
 
# sh shell
RUN mkdir /magpie
RUN mkdir /magpie/bin
RUN cp /usr/sbin/bash /magpie/bin/
 
# Define magpie as a recognised ssh user                                                                      
RUN echo "Match User magpie" >> /etc/ssh/sshd_config

# file oranization                                                                                            
                                                                                                              
                                                                                                              
        #/root/strace (original)        (1)                                                                   
        #/root/followme                 (2)                                                                   
                                                                                                              
        #/sbin/strace (w-strace)        (3)                                                                   
                                                                                                              
        #/home/user/locked-secret       (4)                                                                   
                                                                                                              
# manual permissions:                                                                                         
                                                                                                              
        #/bin/strace (w-strace) needs no password sudo permissions.     (5)                                   
        #pygmy ALL=(ALL) NOPASSWD:  /home/pygmy/ucsec/ctf-2022/followme/w-strace -f ./*                       
                                                                                                              
                                                                                                              
# (1)
RUN /bin/bash -c "mv /usr/sbin/strace /root/"                                                   

# (2)    
COPY ./app/followme /root/followme

# (3)    
COPY ./app/w-strace /usr/sbin/strace

# (4)                                         
COPY ./app/locked-secret /home/magpie/

# (5)
RUN /bin/bash -c "echo \"magpie ALL=(ALL) NOPASSWD:  /usr/sbin/strace -f ./*\" >> /etc/sudoers"

# testing
#COPY ./app/unlocked-secret /home/magpie/

EXPOSE 22                                                                                                     
CMD ["/usr/sbin/sshd", "-D"]  
