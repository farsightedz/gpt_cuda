__global__ void matrixMulKernel(float *A, float *B, float *C, int width) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (row < width && col < width) {
        float value = 0.0f;
        for (int k = 0; k < width; ++k) {
            value += A[row * width + k] * B[k * width + col];
        }
        C[row * width + col] = value;
    }
}
\n
__global__ void matrixMulKernel(float *A, float *B, float *C, int width) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    __shared__ float As[16][16];
    __shared__ float Bs[16][16];

    for (int k = 0; k < width / 16; ++k) {
        As[threadIdx.y][threadIdx.x] = A[row * width + k * 16 + threadIdx.x];
        Bs[threadIdx.y][threadIdx.x] = B[(k * 16 + threadIdx.y) * width + col];
        __syncthreads();
        float value = 0.0f;
        for (int n = 0; n < 16; ++n) {
            value += As[threadIdx.y][n] * Bs[n][threadIdx.x];
        }
        C[row * width + col] += value;
    }
}