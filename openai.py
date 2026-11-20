from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
)
response = client.chat.completions.create(
    model="qwen2.5-0.5b-instruct",
    messages=[
        { "role": "system", "content": "Ты полезный ассистентю Отвечай кратко на русском языку"},
        {"role": "user", "content": "Объясни разницу между list и tuple в Python"},
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)
