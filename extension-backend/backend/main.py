from fastapi import FastAPI, Query
from ragmodel import answer_question
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from auth import create_access_token, verify_token
from fastapi import HTTPException
from ragmodel import answer_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "admin123":
        token = create_access_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/protected-endpoint")
def protected_route(user=Depends(verify_token)):
    return {"message": "You're authenticated!", "user": user}

@app.get("/")
def root():
    return {"status": "API is running!"}

@app.post("/query")
def query(video_url: str = Query(...), question: str = Query(...)):
    response = answer_question(video_url, question)
    return {"answer": response}
