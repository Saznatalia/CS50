//Encrypts messages by "rotating" eack letter by "key" positions
//NataliaSaz problem set 2-1 "Caesar" less comfortable level
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
void crypting_caesar(string plaintext, int key);
string get_plain_string(string prompt);

int main(int argc, string argv[])
{
    //Validates that the key from user is a single command-line argument and a possitive number
    if (argc == 2 && isdigit(*(argv[1])))
    {
        int a = atoi(argv[1]);//Converts a string number to an integer
        string original = get_plain_string("plaintext: ");
        crypting_caesar(original, a);
    }
    else
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }
}

//Prompt user for the plain text
string get_plain_string(string prompt)
{
    string c;
    c = get_string("%s", prompt);
    return c;
}

//Prints out rotated (crypted) letters, leaving other symbols and spaces as they are
void crypting_caesar(string plaintext, int key)
{
    printf("ciphertext: ");
    int l = strlen(plaintext);
    for (int i = 0; i < l; i++)
    {
        if (isupper(plaintext[i]))
        {
            printf("%c", (plaintext[i] + key - 65) % 26 + 65);
        }
        else if (islower(plaintext[i]))
        {
            printf("%c", (plaintext[i] + key - 97) % 26 + 97);
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}

