# pip install openai
from openai import OpenAI

client = OpenAI(
    api_key="f134ef280d910459f116ab2ed4635ad549487200",
    base_url="https://api-bdo4yd9ctdxdw8zb.aistudio-app.com/v1"
)

completion = client.chat.completions.create(
    model="default",
    temperature=0.6,
    messages=[
        {"role": "user", "content": "你是什么模型"}
    ],
    stream=True
)

for chunk in completion:
    if hasattr(chunk.choices[0].delta, "reasoning_content") and chunk.choices[0].delta.reasoning_content:
        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
    else:
        print(chunk.choices[0].delta.content, end="", flush=True)