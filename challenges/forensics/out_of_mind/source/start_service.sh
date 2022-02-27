#!/bin/bash

# hopefully this will start and keep a steady service running
/etc/init.d/inetutils-inetd start
/etc/init.d/ssh start -D
sshpass -p 'zkUTe9V$hZwTU&!w' ssh myUser@127.0.0.1
echo 'ssh process stopped :/'
