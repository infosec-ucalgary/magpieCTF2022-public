#include <stdio.h>
#include <stdlib.h>

/*
    I still haven't taken the time to move our super secret flag
    in "flag.txt" out of this directory. For now I've just made
    totally sure nobody can access it.
        - "Pops"
    */

int main()
{
    setvbuf ( stdout, NULL , _IONBF , 0 );
    
    char file_name[] = "./available_flags.txt";
    char desired_flag[64];

    printf("Hi! Welcome to the \"Mom and Pops' Flags\" flag search page!");
    printf("\nPlease enter the name of the flag you wish to purchase: ");

    gets(desired_flag);

    FILE *flags = fopen(file_name, "rb");

    printf("\nOh, sorry! We don't have that flag in stock :(\nHere is a list of the available flags:\n");
    char ch;
    while ((ch = fgetc(flags)) != EOF)
        putchar(ch);

    fclose(flags);
    printf("\nPlease come back later!");

    return 0;
}