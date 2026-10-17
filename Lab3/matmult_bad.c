void multiply(int n, double A[n][n], double B[n][n], double C[n][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) C[i][j] = 0.0;   // zero the row first

        for (int k = 0; k < n; k++) {
            double a = A[i][k];                      // fixed for the whole inner loop
            for (int j = 0; j < n; j++) {
                C[i][j] += a * B[k][j];              // both walk along a row
            }
        }
    }
}