void multiply_good(int n, float A[n][n], float B[n][n], float C[n][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) 
        C[i][j] = 0.0;   
        for (int k = 0; k < n; k++) {
            float a = A[i][k]; // held constant so b can walk on a row
            for (int j = 0; j < n; j++) {
                C[i][j] += a * B[k][j]; // B walks on row
            }
        }
    }
}



void multiply_bad(int n, float A[n][n], float B[n][n], float C[n][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) 
        C[i][j] = 0.0;   
        for (int k = 0; k < n; k++) {
            for (int j = 0; j < n; j++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}