#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

void print_preference();
void swap(int *a, int *b);
bool is_cycle(int from, int to);
// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    int candidate_id = -1;
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            candidate_id = i;
        }
    }
    if (candidate_id == -1)
    {
        return false;
    }
    ranks[rank] = candidate_id;
    return true;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // Update preferences array
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

void print_preference()
{
    // printf("Preference: \n");
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            // printf("%i ", preferences[i][j]);
        }
        // printf("\n");
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    print_preference();
    for (int i = 0;  i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                // printf("winner = %i \n", pairs[pair_count].winner);
                pairs[pair_count].loser = j;
                // printf("loser = %i \n", pairs[pair_count].loser);
                pair_count++;
            }

        }
    }
    // printf("%i\n", pair_count);
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // Create strength array based on preferences 2d array
    int strength_array[pair_count];
    for (int i = 0; i < pair_count; i++)
    {
        int winner_votes = preferences[pairs[i].winner][pairs[i].loser];
        int loser_votes = preferences[pairs[i].loser][pairs[i].winner];
        int strength = winner_votes - loser_votes;
        strength_array[i] = strength;
        // printf("%i ", strength_array[i]);
    }

    // Sort the pairs based on strength_array
    for (int j = 0; j < pair_count; j++)
    {
        for (int k = 0; k < pair_count - j - 1; k++)
        {
            if (strength_array[j] < strength_array[j + 1])
            {
                swap(&strength_array[j], &strength_array[j + 1]);
                swap(&pairs[j].winner, &pairs[j + 1].winner);
                swap(&pairs[j].loser, &pairs[j + 1].loser);
            }
        }
    }

    return;
}

void swap(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

void print_pairs();

void print_pairs()
{
    // printf("Sorted pairs: \n");
    for (int i = 0; i < pair_count; i++)
    {
        printf("#%i: ", i);
        printf("%i ", pairs[i].winner);
        printf("%i ", pairs[i].loser);
        printf("\n");
    }
}

void print_lock();

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // print_pairs();
    for (int i = 0; i < pair_count; i++)
    {
        int path[MAX];
        pair p = pairs[i];
        if (is_cycle(p.winner, p.loser))
        {
            // printf("Cycle\n");
            continue;
        }
        locked[p.winner][p.loser] = true;
        // printf("LOCKED: %i %i\n", p.winner, p.loser);

    }
    print_lock();
}

void print_lock()
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            printf("%d ", locked[i][j]);
        }
        printf("\n");
    }
}

bool is_cycle(int from, int to)
{
    if (from == to)
    {
        return true;
    }

    for (int i = 0; i < pair_count; i++)
    {
        if (locked[to][i] == true)
        {
            return is_cycle(from, i);
        }
    }
    return false;
}

bool check_winner(int a);

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (check_winner(i) == true)
        {
            printf("%s\n", candidates[i]);
        }
    }
    return;
}

bool check_winner(int a)
{
    for (int i = 0; i < pair_count; i++)
    {
        if (!locked[i][a] == 0)
        {
            return false;
        }
    }
    return true;
}
