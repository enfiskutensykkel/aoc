#include <immintrin.h>
#include <x86intrin.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_W 1024
#define MAX_H 1024

#include <emmintrin.h>
#include <tmmintrin.h>

// used to read data in from file, not used after that
static char in_data[MAX_H * MAX_W];

// holds the entire map/grid in a "blockwise" format
static char blocks[(MAX_H * MAX_W) / 64][64];

static int indices_north[(MAX_H * MAX_W) / 64]; // order of blocks when rotated 0 degrees
static int indices_west[(MAX_H * MAX_W) / 64]; // order of blocks when rotated 90 degrees
static int indices_south[(MAX_H * MAX_W) / 64]; // order of blocks when rotated 90 degrees
static int indices_east[(MAX_H * MAX_W) / 64]; // order of blocks when rotated 90 degrees


static void blockify(int width, int height)
{
    int v_blocks = height / 8; // how many blocks vertically
    int h_blocks = width / 8; // how many blocks horizontally

    for (int i = 0; i < (height * width); ++i) {
        int g_row = i / width; // row in the grid
        int g_col = i % width; // column in the grid

        int block = (g_row / 8) * h_blocks + (g_col / 8);

        blocks[block][(g_row % 8) * 8 + (g_col % 8)] = in_data[i];
    }

    // Calculate block indices
    for (int row = 0; row < v_blocks; ++row) {
        for (int col = 0; col < h_blocks; ++col) {
            indices_north[row * h_blocks + col] = row * h_blocks + col;
            indices_south[row * h_blocks + col] = (v_blocks - row - 1) * h_blocks + (h_blocks - col - 1);

            indices_west[col * v_blocks + (v_blocks - row - 1)] = row * h_blocks + col;
            indices_east[col * v_blocks + (v_blocks - row - 1)] = (v_blocks - row - 1) * h_blocks + (h_blocks - col - 1);
        }
    }
}


static inline
int score_block(int block, int offset)
{
    __m128i row_result = _mm_setzero_si128();

    // Load row data
    __m128i row0 = _mm_load_si128((__m128i*) &blocks[block][0]);
    __m128i row1 = _mm_load_si128((__m128i*) &blocks[block][16]);
    __m128i row2 = _mm_load_si128((__m128i*) &blocks[block][32]);
    __m128i row3 = _mm_load_si128((__m128i*) &blocks[block][48]);

    // We need to offset the row calculations
    __m128i row_offset = _mm_set_epi16(
        offset, offset, offset, offset,
        offset, offset, offset, offset
    );

    // Exctract all 'O's and mask out their respective row values
    // cmpeq sets all 0xFF if values are equal, so we can mask
    // out the integer value we need per row
    __m128i cmp = _mm_set_epi8(
        'O', 'O', 'O', 'O', 
        'O', 'O', 'O', 'O', 
        'O', 'O', 'O', 'O', 
        'O', 'O', 'O', 'O'
    );

    __m128i mask0 = _mm_set_epi8(
        7, 7, 7, 7, 7, 7, 7, 7,
        8, 8, 8, 8, 8, 8, 8, 8
    );
    __m128i mask1 = _mm_set_epi8(
        5, 5, 5, 5, 5, 5, 5, 5,
        6, 6, 6, 6, 6, 6, 6, 6
    );
    __m128i mask2 = _mm_set_epi8(
        3, 3, 3, 3, 3, 3, 3, 3,
        4, 4, 4, 4, 4, 4, 4, 4
    );
    __m128i mask3 = _mm_set_epi8(
        1, 1, 1, 1, 1, 1, 1, 1,
        2, 2, 2, 2, 2, 2, 2, 2
    );

    row0 = _mm_and_si128(mask0, _mm_cmpeq_epi8(cmp, row0));
    row1 = _mm_and_si128(mask1, _mm_cmpeq_epi8(cmp, row1));
    row2 = _mm_and_si128(mask2, _mm_cmpeq_epi8(cmp, row2));
    row3 = _mm_and_si128(mask3, _mm_cmpeq_epi8(cmp, row3));

    // Unpack to 16 bit, add offset, and add to final result
    // FIXME: mask offset, so that we don't add offset to every cell, but only the ones that have a value
    // use some cmp > 0 instruction
    row_result = _mm_add_epi16(row_result, _mm_add_epi16(row_offset, _mm_unpacklo_epi8(row3, _mm_setzero_si128())));
    row_result = _mm_add_epi16(row_result, _mm_add_epi16(row_offset, _mm_unpackhi_epi8(row3, _mm_setzero_si128())));

    row_result = _mm_add_epi16(row_result, _mm_add_epi16(row_offset, _mm_unpacklo_epi8(row2, _mm_setzero_si128())));
    row_result = _mm_add_epi16(row_result, _mm_add_epi16(row_offset, _mm_unpackhi_epi8(row2, _mm_setzero_si128())));

    row_result = _mm_add_epi16(row_result, _mm_add_epi16(row_offset, _mm_unpacklo_epi8(row1, _mm_setzero_si128())));
    row_result = _mm_add_epi16(row_result, _mm_add_epi16(row_offset, _mm_unpackhi_epi8(row1, _mm_setzero_si128())));
    
    row_result = _mm_add_epi16(row_result, _mm_add_epi16(row_offset, _mm_unpacklo_epi8(row0, _mm_setzero_si128())));
    row_result = _mm_add_epi16(row_result, _mm_add_epi16(row_offset, _mm_unpackhi_epi8(row0, _mm_setzero_si128())));

    // Unpack to 32 bit, add together, unpack to 64 bit, add together
    __m128i result_lo = _mm_unpacklo_epi16(row_result, _mm_setzero_si128());
    __m128i result_hi = _mm_unpackhi_epi16(row_result, _mm_setzero_si128());
    row_result = _mm_add_epi32(result_lo, result_hi);

    result_lo = _mm_unpacklo_epi32(row_result, _mm_setzero_si128());
    result_hi = _mm_unpackhi_epi32(row_result, _mm_setzero_si128());

    row_result = _mm_add_epi32(result_lo, result_hi);

    result_lo = _mm_unpacklo_epi64(row_result, _mm_setzero_si128());
    result_hi = _mm_unpackhi_epi64(row_result, _mm_setzero_si128());

    row_result = _mm_add_epi32(result_lo, result_hi);

    return _mm_cvtsi128_si32(row_result);
}

static inline
void rotate_block(int block)
{
    // Load block rows (2 rows per variable -> "double row")
    __m128i dr0 = _mm_load_si128((__m128i*) &blocks[block][0]);
    __m128i dr1 = _mm_load_si128((__m128i*) &blocks[block][16]);
    __m128i dr2 = _mm_load_si128((__m128i*) &blocks[block][32]);
    __m128i dr3 = _mm_load_si128((__m128i*) &blocks[block][48]);

    // Interleave 4x4 using _mm_shuffle_ps
    // We need to cast to floats and back again
    __m128i tr0 = _mm_castps_si128(
        _mm_shuffle_ps(
            _mm_castsi128_ps(dr0),
            _mm_castsi128_ps(dr1),
            0x88 
        )
    );
    __m128i tr1 = _mm_castps_si128(
        _mm_shuffle_ps(
            _mm_castsi128_ps(dr2),
            _mm_castsi128_ps(dr3),
            0x88
        )
    );
    __m128i tr2 = _mm_castps_si128(
        _mm_shuffle_ps(
            _mm_castsi128_ps(dr0),
            _mm_castsi128_ps(dr1),
            0xdd 
        )
    );
    __m128i tr3 = _mm_castps_si128(
        _mm_shuffle_ps(
            _mm_castsi128_ps(dr2),
            _mm_castsi128_ps(dr3),
            0xdd
        )
    );

    // Shuffle interleaved data around
    __m128i pshufb_interleave = _mm_set_epi8(
        15, 11,  7,  3,
        14, 10,  6,  2,
        13,  9,  5,  1,
        12,  8,  4,  0
    );
    dr0 = _mm_shuffle_epi8(tr0, pshufb_interleave);
    dr1 = _mm_shuffle_epi8(tr1, pshufb_interleave);
    dr2 = _mm_shuffle_epi8(tr2, pshufb_interleave);
    dr3 = _mm_shuffle_epi8(tr3, pshufb_interleave);

    // Unpack shuffled data
    tr0 = _mm_unpacklo_epi32(dr0, dr1);
    tr1 = _mm_unpackhi_epi32(dr0, dr1);
    tr2 = _mm_unpacklo_epi32(dr2, dr3);
    tr3 = _mm_unpackhi_epi32(dr2, dr3);

    // Reverse columns
    __m128i pshufb_reverse = _mm_set_epi8(
        8,  9, 10, 11, 12, 13, 14, 15,
        0,  1,  2,  3,  4,  5,  6,  7
    );
    dr0 = _mm_shuffle_epi8(tr0, pshufb_reverse);
    dr1 = _mm_shuffle_epi8(tr1, pshufb_reverse);
    dr2 = _mm_shuffle_epi8(tr2, pshufb_reverse);
    dr3 = _mm_shuffle_epi8(tr3, pshufb_reverse);

    // Store rotated block
    _mm_store_si128((__m128i*) &blocks[block][0], dr0);
    _mm_store_si128((__m128i*) &blocks[block][16], dr1);
    _mm_store_si128((__m128i*) &blocks[block][32], dr2);
    _mm_store_si128((__m128i*) &blocks[block][48], dr3);
}


static void rotate(int width, int height)
{
    int h_blocks = (width / 8);
    int v_blocks = (height / 8);

    for (int i = 0; i < (h_blocks * v_blocks); ++i) {
        rotate_block(i);
    }
}


static void tilt(int width, int height, const int *indices)
{
    int w = width;
    int h = height;

    if (indices == indices_east || indices == indices_west) {
        w = width;
        h = height;
    }

    int h_blocks = (w / 8);

    for (int col = 0; col < w; ++col) {
        for (int row = 0; row < h; ++row) {
            int block = indices[(row >> 3) * h_blocks + (col >> 3)];

            if (blocks[block][((row & 7) << 3) + (col & 7)] == 'O') {

                int move_row = row;
                int move_block = block;

                while (true) {
                    int test_row = move_row - 1;

                    if (test_row < 0) {
                        break;
                    }

                    int test_block = indices[(test_row >> 3) * h_blocks + (col >> 3)];
                    if (blocks[test_block][((test_row & 7) << 3) + (col & 7)] != '.') {
                        break;
                    }

                    move_block = test_block;
                    move_row = test_row;
                }
                
                if (move_row != row) {
                    blocks[block][((row & 7) << 3) + (col & 7)] = '.';
                    blocks[move_block][((move_row & 7) << 3) + (col & 7)] = 'O';
                }
            }
        }
    }
}


static unsigned long long score_blocks(int width, int height, int real_height)
{
    int h_blocks = width / 8;
    int v_blocks = height / 8;

    unsigned long long score = 0;

    for (int i = 0; i < (h_blocks * v_blocks); ++i) {
        int offset = real_height - 8 * (i / v_blocks) - 8;
        int block_score = score_block(i, offset);
        score += block_score;
    }

    return score;
}


static void print_blocks(int width, int height, const int *indices)
{
    int w = width;
    int h = height;

    if (indices == indices_east || indices == indices_west) {
        w = height;
        h = width;
    }

    int h_blocks = w / 8;

    for (int r = 0; r < h; ++r) {
        //printf("%4d ", r+1);

        for (int c = 0; c < w; ++c) {
            int block = indices[(r / 8) * h_blocks + (c / 8)];

            printf("%c", blocks[block][(r % 8) * 8 + (c % 8)]);
        }

        printf("\n");
    }
}


static void spin_cycle(int width, int height)
{
    tilt(width, height, indices_north);
    rotate(width, height);
    tilt(width, height, indices_west);
    rotate(width, height);
    tilt(width, height, indices_south);
    rotate(width, height);
    tilt(width, height, indices_east);
    rotate(width, height);
}



int main()
{
    char *line = NULL;
    ssize_t len = 0;
    size_t size;

    int real_height = 0;
    int width = 0;
    int height = 0;

    // Read grid from file into row-major format
    while ((len = getline(&line, &size, stdin)) != -1) {

        if ((len-1) >= MAX_W) {
            fprintf(stderr, "grid is too wide\n");
            return 1;
        }

        if (height >= MAX_H) {
            fprintf(stderr, "grid is too high\n");
            return 1;
        }

        int real_width = len - 1;

        // Round width up to a multiple if 8
        width = (real_width + 7) & ~7;

        memcpy(&in_data[height * width], line, real_width);

        // Align to block width
        for (int i = real_width; i < width; ++i) {
            in_data[height * width + i] = '#'; // '#' is a non-moving rounded cube
        }

        ++height;
    }

    free(line); // don't need this anymore

    // Align to block height
    real_height = height;
    while (height % 8 != 0) {
        for (int i = 0; i < width; ++i) {
            in_data[height * width + i] = '#';
        }
        ++height;
    }

    // Store in "block format" so we can easily transpose it 8x8
    blockify(width, height);

    //tilt(width, height, indices_north);
    print_blocks(width, height, indices_north);

    unsigned long long score = score_blocks(width, height, real_height);

    printf("%llu\n", score);

    return 0;
}
