import openai

from zhipuai import ZhipuAI

def generate_suggestions(ncu_output_file, suggestion_json_file):
    # 读取 Ncu_output.txt 的内容
    with open(ncu_output_file, 'r', encoding='utf-8') as file:
        ncu_output = file.read()
    
    # 构建提示信息
    prompt = f"""请根据以下 NCU 输出，分析存在的问题并生成优化建议，格式为 JSON，包括 "ProblemAnalysis" 和 "OptimizationMethods"。

NCU 输出：

{ncu_output}

请按以下格式生成 suggestion.json 的内容：

{{
    "ProblemAnalysis": [
        {{
            "Issue": "描述问题",
            "Data": {{
                "相关数据": "值"
            }},
            "Analysis": "对问题的详细分析"
        }},
        ...
    ],
    "OptimizationMethods": [
        {{
            "step": 步骤编号,
            "Method": "优化方法名称",
            "Actions": [
                "具体行动方案1",
                "具体行动方案2",
                ...
            ]
        }},
        ...
    ]
}}
"""

    # 设置 OpenAI API 密钥
    # openai.api_key = 'your_api_key_here' 

    # # 调用 OpenAI API
    # response = openai.Completion.create(
    #     engine='text-davinci-003',  # 选择模型
    #     prompt=prompt,
    #     max_tokens=2048,
    #     temperature=0.7,
    #     n=1,
    #     stop=None,
    # )
    client = ZhipuAI(api_key="118811ab3230dcce2d67597afacadc78.n130hcT8A0FOdqc1")
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        top_p=0.7,
        temperature=0.9,
        stream=False,
        max_tokens=5000,
    )

    # 获取生成的文本
    generated_text = response.choices[0].message.content.strip()

    # 检查并移除 ```json 和 ``` 代码块标记
    if generated_text.startswith("```json"):
        generated_text = generated_text[len("```json"):].strip()
    if generated_text.endswith("```"):
        generated_text = generated_text[:-len("```")].strip()

    # 将生成的文本保存为 suggestion.json
    with open(suggestion_json_file, 'w', encoding='utf-8') as file:
        file.write(generated_text)

if __name__ == "__main__":
    ncu_output_file = 'Ncu_output.txt'
    suggestion_json_file = 'suggestion3.json'
    generate_suggestions(ncu_output_file, suggestion_json_file)