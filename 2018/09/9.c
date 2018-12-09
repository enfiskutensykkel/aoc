#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

struct marble
{
    struct marble*  next;
    struct marble*  prev;
    uint32_t        value;
};


int insert_marble(struct marble** current, uint32_t value)
{
    struct marble* marble = malloc(sizeof(struct marble));
    if (marble == NULL) {
        return 1;
    }

    marble->value = value;
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

    if (ptr != NULL) {
        uint32_t value = ptr->value;
        *current = ptr->next;
        if (ptr == *current) {
            *current = NULL;
        }
        ptr->next->prev = ptr->prev;
        ptr->prev->next = ptr->next;
        free(ptr);
        return value;
    }

    return 0;
}

uint64_t play_game(int players, uint32_t last_marble)
{
    uint64_t* scores = calloc(players, sizeof(uint64_t));
    if (scores == NULL) {
        return 0;
    }

    struct marble* current = malloc(sizeof(struct marble));
    if (current == NULL) {
        free(scores);
        return 0;
    }
    current->value = 0;
    current->next = current;
    current->prev = current;

    int player = 0;
    uint32_t next_marble = 1;
    while (current->value != last_marble) {
        if (next_marble % 23 == 0) {
            scores[player] += next_marble;
            scores[player] += remove_marble(&current);
        } else {
            insert_marble(&current, next_marble);
        }

        ++next_marble;
        player = (player + 1) % players;
    }

    current->prev->next = NULL;
    while (current != NULL) {
        struct marble* next = current->next;
        free(current);
        current = next;
    }

    uint64_t max = 0;
    for (int i = 0; i < players; ++i) {
        if (scores[i] > max) {
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
    printf("%llu\n%llu\n", part1, part2);
    return 0;
}
