# YouTube Transcript Q&A Extension  
(OpenAI + LangChain + FAISS)

A browser extension that enables question-answering directly on YouTube videos using a Retrieval-Augmented Generation (RAG) pipeline. The extension automatically extracts the video transcript, processes it into vector embeddings, and generates accurate, context-aware answers grounded strictly in the video content.

---

## Features

- Automatic YouTube transcript extraction  
- Semantic chunking of transcript text  
- Embedding generation using OpenAI  
- Vector storage and similarity search with FAISS  
- Structured RAG pipeline using LangChain Runnables  
- Context-aware question answering based on the video transcript  

---

## Tech Stack

- Python 3.10+  
- LangChain  
- OpenAI API  
- FAISS  
- YouTube Transcript API  

---

## High-Level Workflow

1. Extract transcript from the active YouTube video  
2. Split transcript into semantic chunks  
3. Generate embeddings using OpenAI  
4. Store and retrieve embeddings via FAISS  
5. Generate grounded answers using a RAG pipeline  

---

