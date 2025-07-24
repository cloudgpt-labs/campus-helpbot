# app.py

import os
import openai
import json
from dotenv import load_dotenv

# Load environment variables from .env (if present)
load_dotenv()

# === Azure OpenAI Config ===
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")          # e.g., https://your-resource.openai.azure.com/
openai.api_version = "2024-02-15-preview"                     # Latest recommended
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")   # e.g., "gpt-35-turbo"

# === Load Prompt Template ===
with open("prompt_template.txt", "r") as file:
    prompt_template = file.read()

# === Load Sample FAQ Context ===
with open("sample_faq.json", "r") as file:
    faq_data = json.load(file)

faq_context = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in faq_data])

# === Interactive CLI Loop ===
print("🎓 Welcome to Campus HelpBot! (type 'exit' to quit)\n")

while True:
    user_input = input("🧑 You: ")

    if user_input.strip().lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Combine template with context and user question
    full_prompt = prompt_template.format(context=faq_context, question=user_input)

    try:
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for university students."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message['content'].strip()
        print(f"\n🤖 HelpBot: {reply}\n")

    except Exception as e:
        print("⚠️ Error:", e)
