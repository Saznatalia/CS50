// Returns minimum number of coins with which that change can be made
// NataliaSaz problem set 1-3 "Cash" less comfortable level
#include <cs50.h>
#include <stdio.h>
#include <math.h>
float get_positive_float(string prompt);
void print_coins(float change);

int main(void)
{
    float i = get_positive_float("Change: $");
    print_coins(i);
}

// Prompt user for change
float get_positive_float(string prompt)
{
    float n;
    do
    {
        n = get_float("%s", prompt);
    }
    while (n <= 0);
    return n;
}

// Calculates minimum number of coins
void print_coins(float change)
{
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    int cents = round(change * 100);
    int qty_of_quarters = cents / quarter;
    int qty_of_dimes = (cents - qty_of_quarters * quarter) / dime;
    int qty_of_nickels = (cents - qty_of_quarters * quarter - qty_of_dimes * dime) / nickel;
    int qty_of_pennies = (cents - qty_of_quarters * quarter - qty_of_dimes * dime - qty_of_nickels * nickel) / penny;
    int coins = qty_of_quarters + qty_of_dimes + qty_of_nickels + qty_of_pennies;
    printf("Number of coins: %i\n", coins);
}
