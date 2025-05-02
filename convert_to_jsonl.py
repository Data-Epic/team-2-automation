# convert_to_jsonl.py
import pandas as pd
import json

# Loading labeled CSV file
df = pd.read_csv("data/sentiment_training_data.csv")

# Converting and writing to JSONL
with open("data/train_data.jsonl", "w") as f:
    for _, row in df.iterrows():
        json.dump({"text": row["text"], "label": row["label"]}, f)
        f.write("\n")

print("✅ JSONL file created successfully.")
