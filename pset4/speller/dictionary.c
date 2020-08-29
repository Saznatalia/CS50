// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

int count = 0;

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

node *head;
// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate a memore for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }
        // Copy word into new node
        strcpy(new_node -> word, word);
        // Hash word based on fisrt letter
        int hash_head = hash(word);
        // Insert new node into linked list
        if (hashtable[hash_head] == NULL)
        {
            new_node -> next = NULL; // Pointer "next" points to null
            hashtable[hash_head] = new_node;// Pointer hash_head points to new node
        }
        else
        {
            new_node -> next = hashtable[hash_head]; // Pointer "next" from new node points to same place where hash_head points to
            hashtable[hash_head] = new_node; // Pointer hash_head points to new node
        }

        count++;


    }
    printf("Size: %i\n", count);

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (count > 0)
    {
        return count;
    }
    return 0;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash the word
    int hash_head = hash(word);
    // Create a node pointer head that points to first element of linked list
    head = hashtable[hash_head];
    // create a node pointer cursor that points to same element as pointer head
    node *cursor = head;
    while (cursor != NULL)
    {
        char *temp = cursor -> word;
        if (strcasecmp(word, temp) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // create a node pointer cursor that points to same element as pointer head
    node *cursor = head;
    while (cursor != NULL)
    {
        node *temp = cursor;
        cursor = cursor -> next;
        free(temp);
    }
    return true;
}
