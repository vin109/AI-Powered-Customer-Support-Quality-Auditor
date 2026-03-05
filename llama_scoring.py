import pandas as pd
import ollama
import json
import os
import re

# ----------------------------
# Load your preprocessed data
# ----------------------------
df = pd.read_csv("preprocessed_calls.csv")


def llm_score(transcript):
    """
    Sends transcript to local Llama model and returns structured scoring.
    """

    prompt = f"""
You are a data extraction system.

Return ONLY valid JSON.
Do NOT write explanations.
Do NOT write sentences.
Do NOT add text before or after JSON.

Output format:

{{ 
 "empathy": integer,
 "urgency": integer,
 "politeness": integer,
 "reason": "one short sentence"
}}

Transcript:
{transcript}
"""

    response = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': prompt}],
        options={
            "temperature": 0
        }
    )

    content = response['message']['content']

    # Extract only JSON part (bulletproof parsing)
    json_match = re.search(r'\{.*\}', content, re.DOTALL)

    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            return {
                "empathy": None,
                "urgency": None,
                "politeness": None,
                "reason": "JSON parsing error"
            }
    else:
        return {
            "empathy": None,
            "urgency": None,
            "politeness": None,
            "reason": "No JSON found"
        }


# ----------------------------------------
# IMPORTANT: Test with small subset first
# ----------------------------------------
subset = df.head(3)   # change to full df after testing

print("Starting Llama scoring...")

scores = subset["clean_transcript"].apply(llm_score)

# Convert JSON results into columns
scores_df = pd.json_normalize(scores)

# Combine original data + AI scores
final_df = pd.concat([subset.reset_index(drop=True), scores_df], axis=1)

# Create output directory if it doesn't exist
os.makedirs("data/", exist_ok=True)

# Save results
final_df.to_csv("data/llama_scored_calls.csv", index=False)

print("✅ Llama scoring completed successfully!")
