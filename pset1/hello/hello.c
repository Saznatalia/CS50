// Says hello to the world
// NataliaSaz problem set 1 - 1
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string name = get_string("What is your name?\n");
    printf("hello, %s\n", name);
}
