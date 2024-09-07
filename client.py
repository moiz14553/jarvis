from openai import OpenAI # type: ignore
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)