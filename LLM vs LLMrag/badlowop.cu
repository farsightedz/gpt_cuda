#include <cuda_runtime.h>
#include <iostream>

__global__ void efficientKernel(float *data, int N) {
    
    float a = 0, b = 0, c = 0, d = 0;
    float e = 0, f = 0, g = 0, h = 0;
    float i = 0, j = 0, k = 0, l = 0;
    float m = 0, n = 0, o = 0, p = 0;
    
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < N) {
        
        a = b + c; d = e + f;
        g = h + i; j = k + l;
        m = n + o; p = a + b;

        data[idx] = p;
    }
}

int main() {
    const int N = 1 << 20;  
    const int threadsPerBlock = 512; 
    const int numBlocks = (N + threadsPerBlock - 1) / threadsPerBlock;

    float *d_data;
    size_t size = N * sizeof(float);

    // 分配设备内存
    cudaMalloc(&d_data, size);

    // 初始化数据
    efficientKernel<<<numBlocks, threadsPerBlock>>>(d_data, N);

    // 同步设备，检查错误
    cudaDeviceSynchronize();

    // 释放设备内存
    cudaFree(d_data);

    return 0;
}
