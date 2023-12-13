#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <stdbool.h>
#include <string.h>

#define MAX_MIRROR_SIZE     ((1UL << 20) / sizeof(uint64_t))


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


void rotate(size_t width, size_t size, uint64_t *pattern)
{
    uint64_t *rotated = calloc(size, sizeof(uint64_t));
    if (rotated == NULL) {
        return;
    }

    size_t height = size / width;
    for (size_t r = 0; r < height; ++r) {
        for (size_t c = 0; c < width; ++c) {
            if (test_bit(pattern, r * width + (width - c - 1))) {
                set_bit(rotated, c * height + r);
            }
        }
    }

    memcpy(pattern, rotated, size*sizeof(uint64_t));
    free(rotated);
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


void do_stuff(size_t width, size_t size, uint64_t *pattern, size_t *part1, size_t *part2)
{
    bool rotated = false;

    ssize_t line1 = reflection(width, size, pattern, false);
    ssize_t line2 = reflection(width, size, pattern, true);
            
    if (line1 == -1) {
        rotated = true;
        rotate(width, size, pattern);
        line1 = reflection(size / width, size, pattern, false);
        *part1 += (line1 + 1) * 100;
    } else {
        *part1 += line1 + 1;
    }

    if (line2 == -1) {
        if (!rotated) {
            rotate(width, size, pattern);
        }
        line2 = reflection(size / width, size, pattern, true);
        *part2 += (line2 + 1) * 100;
    } else {
        *part2 += line2 + 1;
    }
}


int main()
{
    char *line = NULL;
    size_t sz = 0;
    ssize_t len;

    ssize_t w = 0;
    uint64_t *pattern = NULL;
    size_t idx = 0;

    pattern = calloc(MAX_MIRROR_SIZE, sizeof(uint64_t));
    if (pattern == NULL) {
        return 1;
    }

    size_t part1 = 0;
    size_t part2 = 0;

    while ((len = getline(&line, &sz, stdin)) != -1) {
        if (len == 1) {

            do_stuff(w, idx, pattern, &part1, &part2);

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

    do_stuff(w, idx, pattern, &part1, &part2);

    printf("%zu\n", part1);
    printf("%zu\n", part2);

    free(pattern);
    free(line);
    return 0;
}
