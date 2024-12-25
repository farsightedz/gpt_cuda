from zhipuai import ZhipuAI
import re

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


if __name__ == "__main__":
    client = ZhipuAI(api_key="118811ab3230dcce2d67597afacadc78.n130hcT8A0FOdqc1")

    # 使用函数读取并输出.cu文件内容
    file_path = 'new.cu'
    daima = read_cu_file(file_path)


    with open('ncu_output.txt', 'r') as file:
            jianyi = file.read()
    xiugai = jianyi

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {
                "role": "user",
                "content": "请将下面这个cuda代码进行修改“" + daima + "”根据“" + xiugai + "”上面这段话进行修改"
            }
        ],
        top_p=0.7,
        temperature=0.9,
        stream=False,
        max_tokens=2000,
    )

    kk = response.choices[0].message.content
    print(kk)

    code = extract_code(kk)

    with open('new.cu', 'w') as file:
        # 将文本写入文件
        file.write(code)