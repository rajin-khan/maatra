from dotenv import load_dotenv
import os
import json
from groq import Groq

load_dotenv()

# === CONFIG ===
api_key = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"
INPUT_FILE = "nist_ai_rmf_playbook.json"
OUTPUT_FILE = "enriched__govern_policy_sections_4.json"

client = Groq(api_key=api_key)

def generate_prompt(section):
    return f"""
You are a reasoning-based policy agent tasked with helping organizations build AI governance policies that align with the NIST AI Risk Management Framework (NIST AI RMF).

You will receive a single policy section in JSON format (from the RMF playbook). Your goal is to enrich this JSON with three new fields:

1. "query" – A comprehensive list of questions that a policy-building chatbot should ask the user (Must not exceed more than 3 questions, questions must not directly quote sections nor subsections of the playbook, only infer logic and understanding and validation from it).
2. "validator" – Directions to follow for an LLM to judge the answer to the questions perfectly (no code, validator must be a single value, alright if it is detailed, should heavily include logic understood from the playbook json).
3. "answers" - generate an example optimal answer (max 2) that matches the validator and is checked by it for correctness, and an additional invalid answer (must label if the answer is invalid).

Section:
{json.dumps(section, indent=3)}

Only return a valid JSON object with "query", "validator" and "answer" fields. Do NOT return explanations.
"""

def call_groq_chat(prompt):
    chat_completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert in AI governance and NIST RMF compliance checking."},
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content

def parse_json_safe(output):
    try:
        # First try direct JSON parse
        return json.loads(output)
    except json.JSONDecodeError:
        # Try to extract JSON object from the string if wrapped
        try:
            start = output.find('{')
            end = output.rfind('}') + 1
            return json.loads(output[start:end])
        except Exception as e:
            print("⚠️ Secondary parse failed:", str(e))
            return None

def process_sections():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        sections = json.load(f)

    enriched = []

    for i, section in enumerate(sections):
        print(f"\n🔍 Processing section {i+1}/{len(sections)}: {section.get('title')}")
        prompt = generate_prompt(section)
        output = call_groq_chat(prompt)

        result = parse_json_safe(output)

        if result and "query" in result and "validator" in result:
            section["query"] = result["query"]
            section["validator"] = result["validator"]
            enriched.append(section)
        else:
            print(f"⚠️ Skipping section {section.get('title')} due to invalid output:")
            print(output)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=3)
    print(f"\n✅ Done. Output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_sections()