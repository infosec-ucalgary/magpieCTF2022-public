all: locked-secret strace-wrapper followme

followme: followme.c
	gcc followme.c -o followme

locked-secret: locked-secret.c
	gcc locked-secret.c -o locked-secret

strace-wrapper: verify.c w-strace.c
	gcc verify.c w-strace.c -o w-strace -lcrypto

clean:
	rm locked-secret set-permissions w-strace
