#include<sys/wait.h>
#include<sys/types.h>
#include<unistd.h>
#include<stdlib.h>
#include<stdio.h>

void set_attribute() {
        
	// setfattr -n user.checksum -v "3baf9ebce4c664ca8d9e5f6314fb47fb" foo.txt

        int pid = fork();
        
        if (pid == 0){   
		int err;
		char *env[1] = { 0 };
		char *argv[5] = {"-n", "flag", "-v", "magpie{1_gu3sz_y()u_c4ught_m3}", "lockbox.txt"};

		err = execve("/bin/setfattr", argv, env);
		exit(err); //if it got here, it's an error
        } 
        else if(pid<0) {
                exit(-1);
        }

        int status;
        wait(&status);
}

int main() {

	set_attribute();
	printf("You're not fast enough to follow me. \n");
        return 0;
}
