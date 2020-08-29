// Identifies whether the credit card valid
// NataliaSaz problem set 1-3 "Credit" more comfotable level
#include <cs50.h>
#include <stdio.h>
#include <math.h>
long get_positive_long(string prompt);
void check_legit_amex(long number);
void print_legit_amex(long number);
void print_legit_master(long number);
void print_legit_visa(long number);

int main(void)
{
    long number = get_positive_long("Number: ");
    int length_of_long = 1 + log10(number);
    printf("%i\n", length_of_long);
    printf("%li\n", number / 10000000000000);
    if (length_of_long == 15 && ((number / 10000000000000) == 34 || (number / 10000000000000) == 37))
    {
        check_legit_amex(number);
    }
    if (length_of_long == 16 && ((number / 100000000000000) == 51 || (number / 100000000000000) == 52 || (number / 100000000000000) == 53 || (number / 100000000000000) == 54 || (number / 100000000000000) == 55))
    {
        print_legit_master(number);
    }
    if ((length_of_long == 13 && (number / 1000000000000) == 4) || (length_of_long == 16 && (number / 1000000000000000) == 4))
    {
        print_legit_visa(number);
    }
    else
    {
        printf("INVALID\n");
    }
}

// Prompt user for a credit card number
long get_positive_long(string prompt)
{
    long n;
    do
    {
        n = get_long("%s", prompt);
    }
    while (n < 0);
    return n;
}

void check_legit_amex(long number)
{
    int sum = 0;
    for (int i = number - 1; i >= 0; i--)
    {
        if (number % 2 != 0)
        {
            sum = sum + number;
        }
    printf("%i\n", sum);
    }
}

// Validates if the  number is legit
void print_legit_amex(long number)
{
    printf("AMEX\n");
}

void print_legit_master(long number)
{
    printf("MASTERCARD\n");
}

void print_legit_visa(long number)
{
    printf("VISA\n");
}

