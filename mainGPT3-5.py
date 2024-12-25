import openai
import re
import subprocess
from get_json_item import generate_suggestions_text
from create_jsonGPT35 import generate_suggestions
# from dotenv import load_dotenv
# import os
# api_key = os.getenv('API_KEY')

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
            return content_cu
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except IOError:
        print(f"读取文件 {file_path} 时发生错误。")

def use_llm(suggestion_text):
    openai.api_key = "sk-dnO3PZBuZSF7ydVi9AZ6mJ79vaKbcIJX3GSMdnjrxFjl7T7z"
    openai.api_base = "https://sg.uiuiapi.com/v1"

    # 使用函数读取并输出.cu文件内容
    file_path = 'demo.cu'
    daima = read_cu_file(file_path)
    print("已获取代码")

    # 构造提示
    prompt = f"请根据以下 NSight Compute 的分析数据，对给定的 CUDA 代码进行优化修改。\n\nCUDA 代码：\n{daima}\n\n分析数据：\n{suggestion_text}\n\n请输出修改后的代码，仅代码部分即可。"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.9,
        max_tokens=4096,
    )

    kk = response['choices'][0]['message']['content']
    # print(kk)
    return extract_code(kk)
def use_nvcc_ncu():
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
        with open("Ncu_output.txt", "w") as file:
            file.write(output)
        print("Output saved to Ncu_output.txt")

if __name__ == "__main__":

    # 初步分析CUDA代码
    use_nvcc_ncu()

    # 对ncu分析结果进行优化建议Cot
    generate_suggestions('Ncu_output.txt', 'suggestion/ncu_suggestion.json')

    # 对json进行信息提取
    suggestion_text = generate_suggestions_text('suggestion/ncu_suggestion.json')
    # print(suggestion_text)

    # 使用LLM进行代码优化
    code = use_llm(suggestion_text)

    with open('new.cu', 'w') as file:
        # 将文本写入文件
        file.write(code)

    print("已经完成修改,并保存在new.cu中")
