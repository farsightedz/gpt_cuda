import openai
import re
import subprocess
import os


def run_command(command):
    try:
        # 使用 subprocess.run 执行命令
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with return code {e.returncode}")
        print(e.output)
        return None
    
def extract_code(text):
    # 使用正则表达式匹配代码块
    code_blocks = re.findall(r'```(?:cuda|cpp|)(.*?)```', text, re.DOTALL)
    # 将所有代码块拼接成一个字符串
    code = "\\n".join(code_blocks).strip()
    return code

def read_cu_file(file_path):
    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content_cu = file.read()
            print("已获取代码")
            return content_cu
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except IOError:
        print(f"读取文件 {file_path} 时发生错误。")
def use_nvcc_ncu():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(__file__)
    # 使用函数读取并输出.cu文件内容
    file_path = os.path.join(current_dir, '..', 'NcuOutput')
    # 编译 CUDA 代码
    nvcc_command = "nvcc -o demo demo.cu"
    print("Running:", nvcc_command)
    run_command(nvcc_command)
    print("nvcc run over")

    # 运行 ncu 并获取输出
    ncu_command = "ncu --set full --target-processes all ./demo"
    print("Running:", ncu_command)
    output = run_command(ncu_command)
    print("ncu run over,接下来进入GPT优化阶段")

    # 将 ncu 的输出保存到文件
    if output:
        

        output_path =file_path+'\\'+ get_file_name(file_path, False) + "_ncu_output.txt"

        with open(output_path, "w") as file:
            file.write(output)
        print("Output saved to Ncu_output.txt")
    
def get_file_name(file_path, with_extension):
    # 从文件路径中提取文件名
    if with_extension:
        return os.path.basename(file_path)
    else:
        return os.path.splitext(os.path.basename(file_path))[0]
if __name__ == "__main__":
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(__file__)
    # 使用函数读取并输出.cu文件内容
    file_path = os.path.join(current_dir, '..', 'dataset', 'demo.cu')
    print(file_path)
    daima = read_cu_file(file_path)
    print(get_file_name(file_path,True))
    print(get_file_name(file_path,False))
    # 进行ncu分析


    