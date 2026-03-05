import pandas as pd
import re

# Load data
df = pd.read_csv("call_recordings.csv")

# Clean transcript
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["clean_transcript"] = df["Transcript"].apply(clean_text)

# Save preprocessed data
df.to_csv("preprocessed_calls.csv", index=False)

print("Preprocessing complete. File saved as preprocessed_calls.csv")
