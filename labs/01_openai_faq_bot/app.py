# app.py

import os
import openai
import json

# Load API credentials from environment variables
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2023-05-15"

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  # e.g., "gpt-35-turbo"

# Load prompt template
with open("prompt_template.txt", "r") as file:
    prompt_template = file.read()

# Load FAQ context
with open("sample_faq.json", "r") as file:
    faq_data = json.load(file)

context = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in faq_data])

print("🤖 Campus HelpBot (powered by Azure GPT)\nType your question below:")

while True:
    user_input = input("\n You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    full_prompt = prompt_template.format(context=context, question=user_input)

    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for university students."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    reply = response.choices[0].message['content']
    print(f"\n HelpBot: {reply}")
