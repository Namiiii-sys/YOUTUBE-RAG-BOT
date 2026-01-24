from fastapi import FastAPI, Query, Depends, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ragmodel import answer_question
from auth import verify_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for extension access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API is running!"}

@app.post("/query")
def query(video_url: str = Query(...), question: str = Query(...), user: dict = Depends(verify_token)):
    # user dict contains firebase token claims (e.g. user['uid'], user['email'])
    print(f"Authenticated user: {user.get('email', 'unknown')}")
    response = answer_question(video_url, question)
    return {"answer": response}
