import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("Listing available models:")
print("Listing ALL available models:")
for m in genai.list_models():
    print(f"Model: {m.name}")
    print(f"Supported Methods: {m.supported_generation_methods}")
    print("-" * 20)
