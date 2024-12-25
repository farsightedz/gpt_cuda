import subprocess

def run_command(command):
    try:
        # 使用 subprocess.run 执行命令
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with return code {e.returncode}")
        print(e.output)
        return None

if __name__ == "__main__":
    # 编译 CUDA 代码
    # nvcc_command = "nvcc -o vectorAdd vectorAdd.cu"
    # print("Running:", nvcc_command)
    # run_command(nvcc_command)

    # 运行 ncu 并获取输出
    ncu_command = "ncu ./new"
    print("Running:", ncu_command)
    output = run_command(ncu_command)

    # 将 ncu 的输出保存到文件
    if output:
        with open("ncu_output.txt", "w") as file:
            file.write(output)
        print("Output saved to ncu_output.txt")
