"""
test_json.py

Python utility script for:
1. Counting how many samples exist for each sentiment label in a JSONL training dataset.
2. Cleaning the dataset by:
   - Removing whitespace from text and labels.
   - Lowercasing all labels.
   - Keeping only valid labels (positive, negative, neutral).
   - Writing clean examples to a new file.

 Intended to be used with Cohere fine-tuning training data.
"""
#importing neccessary libraries
from collections import Counter
import json

# PART 1: Counting how many samples exist for each label 

# Initializing a counter to track label frequencies
counts = Counter()

# Opening and reading the training data line by line
with open("data/train_data.jsonl", "r") as f:
    for line in f:
        obj = json.loads(line)  # Each line is a separate JSON object
        counts[obj["label"]] += 1  # Counting how many times each label appears

# Printing the label distribution (e.g., {'positive': 100, 'negative': 80, 'neutral': 50})
print("Label counts:", counts)


# PART 2: Cleaning and saveing as a new dataset

input_file = "data/train_data.jsonl"
output_file = "data/train_data_cleaned.jsonl"

# Defining only valid labels
valid_labels = {"positive", "negative", "neutral"}

# Reading from input file and writing cleaned data to output file
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        try:
            obj = json.loads(line)
            text = obj.get("text", "").strip()  # Clean text
            label = obj.get("label", "").strip().lower()  # Clean label

            if label in valid_labels:
                # Write cleaned object to new file
                json.dump({"text": text, "label": label}, outfile)
                outfile.write("\n")
        except json.JSONDecodeError:
            continue  # Skipping all bad lines that can’t be parsed

print("✅ Cleaned data saved to:", output_file)
