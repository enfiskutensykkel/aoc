#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <errno.h>


struct marble
{
    struct marble*  next;
    struct marble*  prev;
    uint32_t        value;
};


int insert_marble(struct marble** current, uint32_t value)
{
    struct marble* marble = malloc(sizeof(struct marble));
    if (marble == NULL) 
    {
        return ENOMEM;
    }

    marble->next = marble;
    marble->prev = marble;
    marble->value = value;

    if (*current == NULL)
    {
        *current = marble;
    }


    marble->next = (*current)->next->next;
    marble->prev = (*current)->next;
    (*current)->next->next->prev = marble;
    (*current)->next->next = marble;
    *current = marble;

    return 0;
}


uint32_t remove_marble(struct marble** current)
{
    struct marble* ptr = *current;

    for (int i = 0; i < 7 && ptr != NULL; ++i, ptr = ptr->prev);

    if (ptr != NULL)
    {
        uint32_t value = ptr->value;
        *current = ptr->next;
        if (ptr == *current)
        {
            *current = NULL;
        }
        ptr->next->prev = ptr->prev;
        ptr->prev->next = ptr->next;
        free(ptr);
        return value;
    }

    return 0;
}


void free_all(struct marble** current)
{
    struct marble* ptr = *current;
    if (*current != NULL)
    {
       ptr = (*current)->next;
    }

    while (ptr != *current)
    {
        struct marble* next = ptr->next;
        free(ptr);
        ptr = next;
    }

    free(*current);
    *current = NULL;
}


uint64_t play_game(int players, uint32_t last_marble)
{
    uint64_t* scores = calloc(players, sizeof(uint64_t));
    if (scores == NULL) 
    {
        return 0;
    }

    struct marble* current = NULL;
    if (insert_marble(&current, 0))
    {
        free(scores);
        return 0;
    }

    int player = 0;
    uint32_t next_marble = 1;
    while (current->value != last_marble)
    {
        if (next_marble % 23 == 0)
        {
            scores[player] += next_marble;
            scores[player] += remove_marble(&current);
        }
        else
        {
            insert_marble(&current, next_marble);
        }

        ++next_marble;
        player = (player + 1) % players;
    }

    free_all(&current);

    // Find maximum score
    uint64_t max = 0;
    for (int i = 0; i < players; ++i) 
    {
        if (scores[i] > max) 
        {
            max = scores[i];
        }
    }

    free(scores);
    return max;
}


int main()
{
    uint64_t part1 = play_game(438, 71626);
    uint64_t part2 = play_game(438, 71626 * 100);

    printf("%llu %llu\n", part1, part2);

    return 0;
}
