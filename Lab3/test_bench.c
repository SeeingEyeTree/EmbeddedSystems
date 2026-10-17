// Testbench for multiply(). Usage: ./tb [n]   (default n = 256)
//
// Build: gcc -O2 -Wall -o tb tb.c multiply.c

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void multiply(int n, double A[n][n], double B[n][n], double C[n][n]);

static double now_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

// Independent dot product for one entry of C.
static double dot(int n, double A[n][n], double B[n][n], int i, int j) {
    double s = 0.0;
    for (int k = 0; k < n; k++) s += A[i][k] * B[k][j];
    return s;
}

int main(int argc, char **argv) {
    int n = (argc > 1) ? atoi(argv[1]) : 256;
    if (n <= 0) {
        fprintf(stderr, "usage: %s [n]\n", argv[0]);
        return 2;
    }

    double (*A)[n] = malloc(sizeof(double[n][n]));
    double (*B)[n] = malloc(sizeof(double[n][n]));
    double (*C)[n] = malloc(sizeof(double[n][n]));
    if (!A || !B || !C) {
        fprintf(stderr, "out of memory for n=%d\n", n);
        return 2;
    }

    // Small integer values: every product and sum is exact in a double,
    // so we can compare results with == and no tolerance.
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            A[i][j] = (i * 7 + j * 3) % 10;
            B[i][j] = (i * 5 + j * 11) % 10;
            C[i][j] = -1.0; // garbage, so we know multiply() overwrote it
        }
    }

    double t0 = now_sec();
    multiply(n, A, B, C);
    double t1 = now_sec();

    int fails = 0;

    // Check 1: sum of all C entries must equal sum_k (colsum of A[:,k]) * (rowsum of B[k,:]).
    // This is O(n^2) and does not use the same loops as multiply().
    double expected = 0.0, actual = 0.0;
    for (int k = 0; k < n; k++) {
        double colA = 0.0, rowB = 0.0;
        for (int i = 0; i < n; i++) colA += A[i][k];
        for (int j = 0; j < n; j++) rowB += B[k][j];
        expected += colA * rowB;
    }
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) actual += C[i][j];
    if (expected != actual) {
        printf("FAIL: sum(C)=%.0f expected %.0f\n", actual, expected);
        fails++;
    }

    // Check 2: spot-check a few individual entries (corners and interior).
    int pts[][2] = {{0, 0}, {0, n - 1}, {n - 1, 0}, {n - 1, n - 1},
                    {n / 2, n / 3}, {n / 3, n / 2}};
    for (size_t p = 0; p < sizeof pts / sizeof pts[0]; p++) {
        int i = pts[p][0], j = pts[p][1];
        double want = dot(n, A, B, i, j);
        if (C[i][j] != want) {
            printf("FAIL: C[%d][%d]=%.0f expected %.0f\n", i, j, C[i][j], want);
            fails++;
        }
    }

    double secs = t1 - t0;
    printf("n=%d  time=%.3f s  (%.3f GFLOP/s)  %s\n",
           n, secs, 2.0 * n * n * n / secs / 1e9, fails ? "FAIL" : "PASS");

    free(A);
    free(B);
    free(C);
    return fails ? 1 : 0;
}