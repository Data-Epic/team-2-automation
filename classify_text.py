"""
classify_text.py

This python script tests a fine-tuned Cohere classification model by passing in sample inputs
and printing out the model's sentiment predictions. Useful it to verify that the Cohere setup (API key, model ID, etc.) is working before running full applications.

"""
#importing neccessary libraries
import cohere  # Cohere API for text classification
import os
from dotenv import load_dotenv  # To load API key from .env

# Loading environment variables from .env file
load_dotenv()

# Getting the Cohere API key from environment
api_key = os.getenv("COHERE_API_KEY")

# Initializing Cohere client
co = cohere.Client(api_key)

# Classifying example texts using fine-tuned model
response = co.classify(
    model="b81a21f8-bb30-4608-825a-db9305344686-ft",  # Replace with your actual model ID
    inputs=["I love this phone", "Battery life is awful"]
)

# Printing out classification results
for classification in response.classifications:
    print(f"Text: {classification.input}")
    print(f"Prediction: {classification.prediction}")
    print("---")
