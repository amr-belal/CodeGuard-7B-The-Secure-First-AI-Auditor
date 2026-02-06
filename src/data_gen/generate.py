import os 
import json
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = """
You are a Senior Security Engineer and Python Expert.
Your goal is to generate training data for a DPO (Direct Preference Optimization) dataset.
For a given security topic, you must provide THREE things:
1. A Prompt: A common user request that usually leads to insecure code.
2. Rejected Code: A naive, functional, but INSECURE solution (e.g., SQLi, hardcoded secrets, no validation).
3. Chosen Code: A secure, production-ready version of the same solution (parameterized queries, env vars, input validation).

Output Format (JSON only):
{
    "prompt": "...",
    "rejected": "...",
    "chosen": "..."
}
Do not include any explanation, just the raw JSON.
"""

def generate_dpo_pair(topic):
    try:
        completion = client.chat.completions.create(
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate a DPO pair for the following security topic: {topic}"}
            ],
            model = "llama-3.1-8b-instant",
            temperature = 0.7,
            response_format = {"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error generating DPO pair for topic '{topic}': {e}")
        return None
    
if __name__ == "__main__":
    topics = ["SQL Injection in Login", "Hardcoded API Keys", "Unvalidated File Upload"]
    dataset = []

    for topic in topics:
        print(f"Generating DPO pair for topic: {topic}")
        data = generate_dpo_pair(topic)
        if data:
            dataset.append(data)

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/sample_dpo.json","w") as f:
        json.dump(dataset, f, indent=4)

    print("DPO dataset generation complete. Sample saved to data/raw/sample_dpo.json")