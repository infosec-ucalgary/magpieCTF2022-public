#include<openssl/sha.h>
#include<sys/types.h>
#include<sys/wait.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<stdio.h>

int checksum(FILE * fileptr) {
 
        char checksum_verification[] = "b38c7b294864d77f6daddc90687b8e277a71ebd35a79dc2e1193a58dcbda7fa3404162fb6b11c481e239339330e8c8d4f56696c7bf046ae9cdc3db7971c82b82";

 
        int bytes;
        int offset = 2;
        SHA512_CTX shaContext;
        char sha512checksum_string[256];
        char * index = sha512checksum_string;
        unsigned char data[1024];
        unsigned char sha512checksum[SHA512_DIGEST_LENGTH];
 
        SHA512_Init (&shaContext);
        while ((bytes = fread(data, 1, sizeof(data), fileptr)) != 0) {
                SHA512_Update(&shaContext, data, bytes);
        }
        SHA512_Final(sha512checksum, &shaContext);
 
        for(int i = 0; i < SHA512_DIGEST_LENGTH; i++) { 
                sprintf(index, "%02x", sha512checksum[i]);
                index += offset;
        }
 
        fclose (fileptr);
 
        if(strcmp(checksum_verification, sha512checksum_string) == 0) { return 0; }
 
        return 1;
}
