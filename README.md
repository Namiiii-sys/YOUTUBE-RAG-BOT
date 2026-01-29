# YouTube Transcript Q&A Extension  
**(LangChain + FAISS + Hugging Face LLM)**

A browser extension that enables **question-answering directly on YouTube videos** using a **Retrieval-Augmented Generation (RAG)** pipeline.  
The extension extracts the video transcript, converts it into vector embeddings, and generates **accurate, context-aware answers grounded strictly in the video content** now with **multilingual support** 

---


## Features

- Secure user authentication using Firebase Authentication with Google OAuth
- Automatic YouTube transcript extraction  
- Semantic chunking of transcript text  
- Embedding generation  
- Vector storage and similarity search using FAISS  
- Structured RAG pipeline using LangChain Runnables  
- **Grounded answers strictly based on the video transcript**  
- **Multilingual Q&A (English, Hindi, Hinglish)**  

---

## Tech Stack

- Python 3.10+
- Firebase Authentication (Google OAuth)
- LangChain  
- **Hugging Face Inference API**  
- **LLaMA-3.1-8B-Instant**  
- FAISS  
- YouTube Transcript API  

---

## High-Level Workflow

1. User signs in using Google OAuth
2. Extract transcript from the active YouTube video  
3. Split transcript into semantic chunks  
4. Generate embeddings  
5. Store and retrieve embeddings via FAISS  
6. Generate grounded answers using a RAG pipeline  

---

## Multilingual Support

The extension intelligently handles:

- **English questions**
- **Hindi questions (native script)**
- **Romanized Hindi (Hinglish)**

All answers are generated **only from the video transcript**, ensuring factual consistency and preventing hallucinations.

---

## Snippets

### Hindi Queries

<p float="left">
  <img src="https://github.com/user-attachments/assets/4e8d38df-5027-4010-b532-993ddc71120c" width="48%" />
  <img src="https://github.com/user-attachments/assets/e04e1cee-61b7-49a0-9578-c2c01497ecb4" width="48%" />
</p>

### English Queries

<p float="center">
  <img src="https://github.com/user-attachments/assets/129904fd-420f-4860-8dbb-16711d3cbb19" width="90%" />
</p>
