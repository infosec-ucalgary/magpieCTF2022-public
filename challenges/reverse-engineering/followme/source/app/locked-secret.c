#include<sys/wait.h>
#include<sys/types.h>
#include<unistd.h>
#include<stdlib.h>
#include<stdio.h>

volatile int x = 0;

void run_at_root() {

	int pid = fork();

        if (pid == 0){
                int err;
                char * env[1] = {NULL};
                err = execve("/root/followme", NULL, NULL); 
                exit(err); 
        } 
        else if(pid < 0) {
                exit(-1);
        }

        int status;
        wait(&status);
}

void main() {

	if (x == 1) {
		run_at_root();
	}

	else {
		printf("You can't force me\n");
	}
}
