#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <stdbool.h>

#define MAX_MIRROR_SIZE     ((1UL << 20) / sizeof(uint64_t))

uint64_t pattern[MAX_MIRROR_SIZE];

uint64_t rotated[MAX_MIRROR_SIZE];


static inline void set_bit(uint64_t *bitmap, size_t i)
{
    bitmap[i / 64] |= 1UL << (i % 64);
}


static inline int test_bit(const uint64_t *bitmap, size_t i)
{
    return !!(bitmap[i / 64] & (1UL << (i % 64)));
}


static inline void clear_bit(uint64_t *bitmap, size_t i)
{
    bitmap[i / 64] &= ~(1UL << (i % 64));
}


void rotate(size_t width, size_t size)
{
    size_t height = size / width;
    for (size_t r = 0; r < height; ++r) {
        for (size_t c = 0; c < width; ++c) {
            if (test_bit(pattern, r * width + c)) { // (width - c - 1))) {
                set_bit(rotated, c * height + r);
            } else {
                clear_bit(rotated, c * height + r);
            }
        }
    }
}


ssize_t reflection(ssize_t width, ssize_t size, const uint64_t *pattern, bool smudge)
{
    ssize_t height = size / width;

    for (ssize_t line = 0; line < width-1; ++line) {
        ssize_t lcol = line;
        ssize_t rcol = line + 1;

        bool smudged = !smudge;

        while (0 <= lcol && rcol < width) {
            for (ssize_t row = 0; row < height; ++row) {
                if (test_bit(pattern, row * width + lcol) != test_bit(pattern, row * width + rcol)) {
                    if (smudged) {
                        goto not_reflecting;
                    }
                    smudged = true;
                }
            }

            --lcol;
            ++rcol;
        }

        if (!smudge || smudged) {
            return line;
        }

not_reflecting:
        ;
    }

    return -1;
}


size_t do_stuff(size_t width, size_t size, bool smudge)
{
    size_t total = 0;
    ssize_t line = 0;

    line = reflection(width, size, pattern, smudge);

    if (line == -1) {
        line = reflection(size / width, size, rotated, smudge);
        total = (line + 1) * 100;
    } else {
        total = line + 1;
    }

    return total;
}


int main()
{
    char *line = NULL;
    size_t sz = 0;
    ssize_t len;

    ssize_t w = 0;
    size_t idx = 0;

    size_t part1 = 0;
    size_t part2 = 0;

    while ((len = getline(&line, &sz, stdin)) != -1) {
        if (len == 1) {
            rotate(w, idx);
            part1 += do_stuff(w, idx, false);
            part2 += do_stuff(w, idx, true);

            idx = 0;
            w = 0;

        } else {
            w = len - 1;

            if ((idx + w) >= MAX_MIRROR_SIZE * sizeof(uint64_t) * 8) {
                fprintf(stderr, "too large pattern: %zu\n", idx + w);
                break;
            }

            for (ssize_t c = 0; c < w; ++c) {
                if (line[c] == '#') {
                    set_bit(pattern, idx);
                } else {
                    clear_bit(pattern, idx);
                }

                ++idx;
            }
        }
    }

    rotate(w, idx);
    part1 += do_stuff(w, idx, false);
    part2 += do_stuff(w, idx, true);

    printf("%zu\n", part1);
    printf("%zu\n", part2);

    free(line);
    return 0;
}
