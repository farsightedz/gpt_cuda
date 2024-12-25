from zhipuai import ZhipuAI

client = ZhipuAI(api_key="118811ab3230dcce2d67597afacadc78.n130hcT8A0FOdqc1")
response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {
            "role": "user",
            "content": "请你作为童话故事大王，写一篇短篇童话故事，故事的主题是要永远保持一颗善良的心，要能够激发儿童的学习兴趣和想象力，同时也能够帮助儿童更好地理解和接受故事中所蕴含的道理和价值观。"
        }
    ],
    top_p=0.7,
    temperature=0.9,
    stream=False,
    max_tokens=2000,
)
print(response.choices[0].message.content)
