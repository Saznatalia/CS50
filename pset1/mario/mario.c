// Builds descending and ascending pyramids for Mario with user-define height
// NataliaSaz problem set 1-3 "Mario" more comfortable level
#include <cs50.h>
#include <stdio.h>
int get_positive_int(string prompt);
void print_hashes(int height);

// Prompt user for height and print required hashes
int main(void)
{
    int i = get_positive_int("Height: ");
    print_hashes(i);
}

// Prompt user for height between [1:8] inclusive
int get_positive_int(string prompt)
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n < 1 || n > 8);
    return n;
}

// Prints ascending & descending pyramids of hatches and spaces
void print_hashes(int height)
{
    for (int i = 0; i < height; i++)
    {
        // Prints left ascending pyramid
        for (int j = 0; j < height; j++)
        {
            if (j < height - i - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        // Prints two spaces between pyramids
        for (int j = height; j <= height + 1; j++)
        {
            printf(" ");
        }
        // Prints right descending pyramid
        for (int j = height + 2; j < 2 * height + 2; j++)
        {
            if (j <= i + height + 2)
            {
                printf("#");
            }

        }
        printf("\n");
    }
}
