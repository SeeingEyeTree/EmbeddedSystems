#include <stdio.h>

void multiply(int n, double A[n][n], double B[n][n], double C[n][n]) {
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            C[i][j] = 0.0; // set zero
            for (int j = 0; j < n; j++) {
                C[i][j] += A[i][k] * B[k][j]; // sum a nad b rows
            }
        }
    }
}
