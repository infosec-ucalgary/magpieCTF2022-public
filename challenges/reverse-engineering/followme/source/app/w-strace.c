#include"verify.h"
#include<sys/types.h>
#include<sys/wait.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<stdio.h>

void execve_wrapper(char * path_cmd, char * argv[]) {

	int pid = fork();

        if (pid == 0){
                int err;
		char * env[1] = {NULL};
                err = execve(path_cmd, argv, env); 
                exit(err); 
        } 
        else if(pid < 0) {
                exit(-1);
        }

        int status;
        wait(&status); 
}

int main(int argc, char ** argv) {

	FILE * fileptr;
	char * filename;

	if (argc == 3 && !strcmp(argv[1], "-f")) {
		filename = argv[2];
		fileptr = fopen(filename, "r");

	}

	else {
		char * strace_p = "/root/strace";
		execve_wrapper(strace_p, argv);
	}

	if (fileptr == NULL) {
		perror("Error while opening the file");
		exit(EXIT_FAILURE);
	}

	if (!checksum(fileptr)) {
		printf("Check succeded.\n");

		char * strace_p = "/root/strace";
		//char * strace_p = "/usr/bin/strace";
		execve_wrapper(strace_p, argv);
		return 0;
	}

	printf("Cannot trace '%s'.\n", filename);

        return 1;
}
