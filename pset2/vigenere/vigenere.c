//Encrypts messages by "rotating" eack letter by its own "key" position
//NataliaSaz problem set 2-2 "Vigenere" less comfortable level
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
bool checking_argv(string input);
void crypting_vigenere(string keyword, string original);
int shift(char c);
void shifting_original(char c, int key);

int main(int argc, string argv[])
{
    //Validates that the key from user is a single command-line argument
    if (argc == 2)
    {
        //Checks if the keyword is letters only
        checking_argv(argv[1]);
        if (checking_argv(argv[1]) == true)
        {
            string original = get_string("plaintext: ");
            crypting_vigenere(original, argv[1]);
        }
        else
        {
            printf("Usage: ./vigenere keyword \n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./vigenere keyword \n");
        return 1;
    }
}
//checking that each letter of argv[1] is alpha
bool checking_argv(string input)
{
    int length_argv = strlen(input);
    for (int i = 0; i < length_argv; i++)
    {
        if (isalpha(input[i]) == 0)
        {
            return false;
        }
    }
    return true;
}
//Shifts letters of keyword into numbers and prints out crypted letters
void crypting_vigenere(string original, string keyword)
{
    printf("ciphertext: ");
    int length_original = strlen(original), length_keyword = strlen(keyword);
    //creates an key array with shifted numbers from keyword
    int key[length_original];
    //iterates through each letter, shiftes to encrypted text
    for (int i = 0, j = 0; i < length_original; i++, j++)
    {
        if (j == length_keyword)
        {
            j = 0;
        }
        if (isalpha(original[i]))
        {
            int key_element = shift(keyword[j]);
            key[i] = key_element;
            shifting_original(original[i], key[i]);
        }
        else
        {
            printf("%c", original[i]);
            j--;
        }
    }
    printf("\n");
}

//Shifts a character into key (integer)
int shift(char c)
{
    if (isupper(c))
    {
        c = c - 65;
    }
    else
    {
        c = c - 97;
    }
    return c;
}

//Prints out shifted letters
void shifting_original(char c, int key)
{
    if (isupper(c))
    {
        printf("%c", (c + key - 65) % 26 + 65);
    }
    else
    {
        printf("%c", (c + key - 97) % 26 + 97);
    }
}
