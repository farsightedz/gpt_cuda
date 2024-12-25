#include <iostream>
#include <cuda_runtime.h>

#define N 1024  // 定义矩阵维度

// CUDA 核函数：矩阵乘法
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
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks((N + threadsPerBlock.x - 1) / threadsPerBlock.x,
                   (N + threadsPerBlock.y - 1) / threadsPerBlock.y);
    
    // 启动 CUDA 核函数
    matrixMulKernel<<<numBlocks, threadsPerBlock>>>(d_A, d_B, d_C, N);
    
    // 将结果从设备传输回主机
    cudaMemcpy(h_C, d_C, matrixSize, cudaMemcpyDeviceToHost);
    
    // 打印结果矩阵
    // printMatrix(h_C, N); // 如需查看结果，可取消注释此行

    // 释放设备内存
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    
    // 释放主机内存
    free(h_A);
    free(h_B);
    free(h_C);
    
    std::cout << "矩阵乘法已完成。" << std::endl;
    
    return 0;
}
