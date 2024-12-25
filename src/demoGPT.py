import openai
from openai import OpenAI


def generate_suggestions():
    api_base = "https://sg.uiuiapi.com/v1"
    api_key = 'sk-59BPSIaWPIw8gH4Zd6jzPJYudOsEzWrgQMKwaVAK0oFddJbD'

    client = OpenAI(api_key=api_key, base_url=api_base)
    with open(ncu_output_file, 'r', encoding='utf-8') as file:
        ncu_output = file.read()

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
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            # {"role": "developer", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    generated_text = completion.choices[0].message.content.strip()
    
    # 检查并移除 ```json 和 ``` 代码块标记
    if generated_text.startswith("```json"):
        generated_text = generated_text[len("```json"):].strip()
    elif generated_text.startswith("```"):
        generated_text = generated_text[len("```"):].strip()

    # 将生成的文本写入 suggestion_json_file
    with open(suggestion_json_file, 'w', encoding='utf-8') as file:
        file.write(generated_text)

ncu_output_file = 'Ncu_output.txt'
suggestion_json_file = 'suggestion.json'
generate_suggestions()