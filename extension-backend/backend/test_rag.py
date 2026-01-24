from ragmodel import answer_question
import os

# Ensure API key is present (mock or real check)
if not os.getenv("GOOGLE_API_KEY"):
    print("Please set GOOGLE_API_KEY in .env")
    exit(1)
    
print("Testing Gemini integration...")
# Use a short video for testing if possible, or just standard flow
# Example: "Me at the zoo" or similar short video
url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" # Me at the zoo
question = "What is the person standing in front of?"
answer = answer_question(url, question)
print(f"Answer: {answer}")
