#include <iostream>
#include <cuda_runtime.h>

#define N 1024          // 定义矩阵维度
#define TILE_WIDTH 16   // 定义块大小

// CUDA 核函数：优化后的矩阵乘法，使用共享内存和循环展开
__global__ void matrixMulKernelOptimized(float *A, float *B, float *C, int width) {
    __shared__ float ds_A[TILE_WIDTH][TILE_WIDTH];  
    __shared__ float ds_B[TILE_WIDTH][TILE_WIDTH];
    int row = blockIdx.y * TILE_WIDTH + threadIdx.y;
    int col = blockIdx.x * TILE_WIDTH + threadIdx.x;

    float value = 0.0f;

    // 分块计算
    for (int m = 0; m < (width + TILE_WIDTH - 1) / TILE_WIDTH; ++m) {
        // 加载A矩阵块到共享内存
        if (row < width && (m * TILE_WIDTH + threadIdx.x) < width)
            ds_A[threadIdx.y][threadIdx.x] = A[row * width + m * TILE_WIDTH + threadIdx.x];
        else
            ds_A[threadIdx.y][threadIdx.x] = 0.0f;

        // 加载B矩阵块到共享内存
        if ((m * TILE_WIDTH + threadIdx.y) < width && col < width)
            ds_B[threadIdx.y][threadIdx.x] = B[(m * TILE_WIDTH + threadIdx.y) * width + col];
        else
            ds_B[threadIdx.y][threadIdx.x] = 0.0f;

        __syncthreads();  // 等待所有线程完成数据加载

        // 计算乘积并累加，使用循环展开优化
        #pragma unroll
        for (int k = 0; k < TILE_WIDTH; ++k) {
            value += ds_A[threadIdx.y][k] * ds_B[k][threadIdx.x];
        }

        __syncthreads();  // 等待所有线程完成计算
    }

    // 将结果写回全局内存
    if (row < width && col < width)
        C[row * width + col] = value;
}

// 辅助函数：初始化矩阵
void initializeMatrix(float *matrix, int width) {
    for (int i = 0; i < width * width; ++i) {
        matrix[i] = static_cast<float>(rand()) / RAND_MAX;
    }
}

// 辅助函数：打印矩阵
void printMatrix(const float *matrix, int width) {
    for (int i = 0; i < width; ++i) {
        for (int j = 0; j < width; ++j) {
            std::cout << matrix[i * width + j] << " ";
        }
        std::cout << std::endl;
    }
}

int main() {
    int matrixSize = N * N * sizeof(float);

    // 分配主机内存
    float *h_A = (float *)malloc(matrixSize);
    float *h_B = (float *)malloc(matrixSize);
    float *h_C = (float *)malloc(matrixSize);

    // 初始化主机矩阵
    initializeMatrix(h_A, N);
    initializeMatrix(h_B, N);

    // 分配设备内存
    float *d_A, *d_B, *d_C;
    cudaMalloc((void **)&d_A, matrixSize);
    cudaMalloc((void **)&d_B, matrixSize);
    cudaMalloc((void **)&d_C, matrixSize);

    // 将数据从主机传输到设备
    cudaMemcpy(d_A, h_A, matrixSize, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, matrixSize, cudaMemcpyHostToDevice);

    // 设置执行配置
    dim3 threadsPerBlock(TILE_WIDTH, TILE_WIDTH);
    dim3 numBlocks((N + TILE_WIDTH - 1) / TILE_WIDTH,
                   (N + TILE_WIDTH - 1) / TILE_WIDTH);

    // 启动优化后的 CUDA 核函数
    matrixMulKernelOptimized<<<numBlocks, threadsPerBlock>>>(d_A, d_B, d_C, N);
    cudaDeviceSynchronize();  // 等待所有线程完成

    // 将结果从设备传输回主机
    cudaMemcpy(h_C, d_C, matrixSize, cudaMemcpyDeviceToHost);

    // 打印结果矩阵（如需查看，请取消以下注释）
    // printMatrix(h_C, N);

    // 释放设备内存
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);

    // 释放主机内存
    free(h_A);
    free(h_B);
    free(h_C);

    std::cout << "优化后的矩阵乘法已完成。" << std::endl;

    return 0;
}