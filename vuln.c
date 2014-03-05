/*
 Spawn a shell...
 From togge

 compile with: gcc vuln.c -o vuln -fno-stack-protector -static -m32

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char buffer[512];

    if (argc != 2)
        printf ("noope\n");
    else
        strcpy(buffer, argv[1]);

    system("/bin/ls");
}
