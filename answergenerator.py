
import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

# === CONFIG ===
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

MODEL = "llama-3.3-70b-versatile"
INPUT_FILE = "./extracted/enriched__govern_policy_sections_4.json"
CONTEXT_FILE = "./extracted/nist_ai_rmf_playbook.json"
OUTPUT_FILE = "./extracted/answer_examples_output2.json"

client = Groq(api_key=api_key)

def load_json(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON file {filepath}: {e}")
        return None

def call_groq(prompt):
    try:
        chat_completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert AI Governance assistant generating example answers from NIST RMF sections."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return None

def parse_json_safe(output_str):
    if not output_str:
        return None
    try:
        return json.loads(output_str)
    except json.JSONDecodeError:
        match = re.search(r"{.*}", output_str, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                return None
    return None

def generate_prompt(context, queries, validator):
    query_list = "\n".join([f"- {q}" for q in queries])
    context_str = json.dumps(context, indent=2)

    return f"""
You are an expert AI Governance assistant specializing in the NIST AI Risk Management Framework (RMF).
You will receive:
- A list of questions
- A playbook section for context
- A validator rule to follow

Your task:
1. Provide TWO valid answers that satisfy the validator and context
2. Provide ONE invalid answer
3. Explain WHY the invalid answer fails (referring to the context or validator)

Return only valid JSON in this format:
{{
  "valid_answers": ["...", "..."],
  "invalid_answer": "...",
  "invalid_reason": "..."
}}

Questions:
{query_list}

Validator:
{validator}

Playbook Context:
{context_str}
"""

def main():
    enriched = load_json(INPUT_FILE)
    playbook = load_json(CONTEXT_FILE)

    if not enriched or not playbook:
        print("❌ Missing required input files.")
        return

    playbook_lookup = {item['title']: item for item in playbook if 'title' in item}
    results = []

    for i, section in enumerate(enriched):
        title = section.get("title")
        print(f"⚙️ Processing: {title} ({i+1}/{len(enriched)})")

        context = playbook_lookup.get(title)
        if not context:
            print(f"⚠️ Skipping: No context found for {title}")
            continue

        queries = section.get("query", [])
        validator = section.get("validator", "")

        if not queries or validator == "N/A":
            print(f"⚠️ Skipping: Missing queries or validator for {title}")
            continue

        prompt = generate_prompt(context, queries, validator)
        response = call_groq(prompt)
        parsed = parse_json_safe(response)

        result = {
            "title": title,
            "queries": queries,
            "validator": validator,
        }

        if parsed and all(k in parsed for k in ("valid_answers", "invalid_answer", "invalid_reason")):
            result.update(parsed)
        else:
            print(f"⚠️ Skipping: Invalid or missing response structure from model for {title}")
            result.update({
                "valid_answers": ["GENERATION FAILED", "GENERATION FAILED"],
                "invalid_answer": "GENERATION FAILED",
                "invalid_reason": "Failed to parse valid output from LLM."
            })

        results.append(result)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Done! Results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
