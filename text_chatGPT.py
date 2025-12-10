from openai import OpenAI
client = OpenAI(key="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")

promt = "Hello world how are you"
completion = client.chat.completions.create(
  model="gpt-5.1",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": promt }
  ]
)

print(completion.choices[0].message)
