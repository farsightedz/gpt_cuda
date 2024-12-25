import openai


def generate_suggestions(ncu_output_file, suggestion_json_file):
    # 读取 Ncu_output.txt 的内容
    with open(ncu_output_file, 'r', encoding='utf-8') as file:
        ncu_output = file.read()
    
    # 构建提示信息
    prompt = f"""请根据以下 Nsight compute(NCU) 输出，分析存在的问题并生成优化建议，格式为 JSON，包括 "ProblemAnalysis" 和 "OptimizationMethods"。

其中NCU 输出为：
"
{ncu_output}
"

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

    api_key = "sk-dnO3PZBuZSF7ydVi9AZ6mJ79vaKbcIJX3GSMdnjrxFjl7T7z"
    api_base = "https://sg.uiuiapi.com/v1"
    client = openai(api_key=api_key, base_url=api_base)

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=4096,
        temperature=0.7,
    )

    # 获取生成的文本
    generated_text = completion['choices'][0]['message']['content'].strip()

    # 检查并移除 ```json 和 ``` 代码块标记
    if generated_text.startswith("```json"):
        generated_text = generated_text[len("```json"):].strip()
    elif generated_text.startswith("```"):
        generated_text = generated_text[3:].strip()
    if generated_text.endswith("```"):
        generated_text = generated_text[:-3].strip()

    # 将生成的文本保存为 suggestion.json
    with open(suggestion_json_file, 'w', encoding='utf-8') as file:
        file.write(generated_text)

if __name__ == "__main__":
    ncu_output_file = 'Ncu_output.txt'
    suggestion_json_file = 'suggestion3.json'
    generate_suggestions(ncu_output_file, suggestion_json_file)