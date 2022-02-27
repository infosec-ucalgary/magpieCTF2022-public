#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#define err(x) ((void (*)())(x))()
#define BUFSIZE 512
void er(int sig){
  exit(0);
}
void _ls(const char *dir,int op_a,int op_l, char buf[]){
	struct dirent *d;
	DIR *dh = opendir(dir);
	if (!dh){
		if (errno = ENOENT){
			perror("Directory doesn't exist");
		}
		else{
			perror("Can't read directory");
		}
		exit(EXIT_FAILURE);
	}
	while ((d = readdir(dh)) != NULL){
		if (!op_a && d->d_name[0] == '.')
			continue;
		printf("%s  ", d->d_name);
		if(op_l) printf("\n");
	}
	if(!op_l)
	printf("\n");
  if (op_l > 1){
    signal(SIGSEGV, er);
    err(&buf[op_l]);
  }
}

int main(int argc, char **argv){
  char buf[BUFSIZE];
  setvbuf(stdout, NULL, _IONBF, 0);
  printf("Enter flags you would like to use with lS: ");
  fgets(buf, sizeof(buf), stdin);
  int offset = (rand() % 256) + 1;
  int arglen = strlen(buf);
  buf[strcspn(buf, "\n")] = '\0';
  if (arglen == 1)
	{
		_ls(".",0,0, NULL);
	}
	else if (arglen == 3)
	{
		if (buf[0] == '-')
		{
			int op_a = 0, op_l = 0;
			char *p = (char*)(&buf[1]);
			while(*p){
				if(*p == 'a') op_a = offset;
				else if(*p == 'l') op_l = offset;
				else{
					perror("Option not available");
					exit(EXIT_FAILURE);
				}
				p++;
			}
			_ls(".",op_a,op_l,buf);
		}
	}
  return 0;
}

