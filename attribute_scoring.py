import pandas as pd
import os

# Load preprocessed data
df = pd.read_csv("preprocessed_calls.csv")

# Empathy-related keywords
EMPATHY_KEYWORDS = [
    "sorry",
    "understand",
    "apologize",
    "i know this is frustrating",
    "i can see why"
]

# Urgency-related keywords
URGENCY_KEYWORDS = [
    "immediately",
    "right away",
    "as soon as possible",
    "priority",
    "urgent"
]

# Politeness-related keywords
POLITENESS_KEYWORDS = [
    "please",
    "thank you",
    "thanks",
    "happy to help",
    "appreciate"
]

def score_attribute(text, keywords):
    count = 0
    for kw in keywords:
        if kw in text:
            count += 1

    if count == 0:
        return 0
    elif count == 1:
        return 1
    else:
        return 2

df["empathy_score"] = df["clean_transcript"].apply(
    lambda x: score_attribute(x, EMPATHY_KEYWORDS)
)

df["urgency_score"] = df["clean_transcript"].apply(
    lambda x: score_attribute(x, URGENCY_KEYWORDS)
)

df["politeness_score"] = df["clean_transcript"].apply(
    lambda x: score_attribute(x, POLITENESS_KEYWORDS)
)

df["soft_skill_score"] = (
    df["empathy_score"]
    + df["urgency_score"]
    + df["politeness_score"]
)

def soft_skill_label(score):
    if score >= 5:
        return "Excellent"
    elif score >= 3:
        return "Acceptable"
    else:
        return "Needs Improvement"

df["soft_skill_label"] = df["soft_skill_score"].apply(soft_skill_label)

# ✅ CREATE DIRECTORY BEFORE SAVING
os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    "data/attribute_scored_calls.csv",
    index=False
)

print("Empathy, urgency, and politeness scoring completed successfully.")
