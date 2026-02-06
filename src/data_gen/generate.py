import os 
import json
from groq import Groq
from dotenv import load_dotenv
import time
from tqdm import tqdm


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TOPIC_GENERATOR_PROMPT = """
Generate a list of 100 distinct Python security vulnerability scenarios.
Each scenario should be a short sentence describing a mistake a developer might make.
Cover diverse areas: Web (Flask/Django), Cloud (AWS/Azure), Crypto, OS, and Data Science.
Format: Just a plain list of sentences, one per line.
"""

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


def get_100_topics():
    print("🎯 Generating 100 security scenarios...")
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": TOPIC_GENERATOR_PROMPT}],
        model="llama-3.3-70b-versatile",
        temperature=0.7
    )
    topics = completion.choices[0].message.content.strip().split('\n')
    
    return [t.split('. ')[-1] if '. ' in t else t for t in topics][:100]


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
    all_topics = get_100_topics()
    dataset = []

   
    for topic in tqdm(all_topics, desc="Building Dataset"):
        data = generate_dpo_pair(topic)
        if data:
            dataset.append(data)
        
       
        time.sleep(1) 

    # الحفظ النهائي
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/full_dataset_100.json", "w") as f:
        json.dump(dataset, f, indent=4)

    print(f"🚀 Success! Generated {len(dataset)} samples.")