

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void multiply_good(int n, float A[n][n], float B[n][n], float C[n][n]);
#define N 1024;
float A[N][N];
float B[N][N];
float C[N][N];


int main() {
    srand((unsigned)time(NULL));
    for(int i = 0; i < N; i++){
        for( int j = 0; j < N; j++){
            A[i][j] = rand()/(float)RAND_MAX;
            B[i][j] = rand()/(float)RAND_MAX;
        }

    }

    clock_t start_time = clock();

    multiply_good(N, A, B,C);

    clock_t end_time = clock();
    float elapse = (float)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("elapse:  %.4f seconds\n", elapse);
    return 0;
}