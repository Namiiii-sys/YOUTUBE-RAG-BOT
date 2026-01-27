from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Prompt Template
prompt = PromptTemplate(
    template="""
    You are a helpful YouTube assistant bot powered by HuggingFace.
    
    INSTRUCTIONS:
    1. **Greetings**: If the user says "Hi", "Hello", "Hey", or similar *opening* greetings, reply with a warm greeting".
    2. **Conversational**: If the user says "Okay", "Thanks", "Cool", etc., reply naturally (e.g., "Let me know if you have more questions!") etc.
    3. **Language & Script Matching (CRITICAL)**: 
       - **Input:** "Hello dost kaise ho" (Romanized Hindi) -> **Output must be:** "Main Bilkul thik hu! aap kaise ho? .." (Romanized Hindi). **DO NOT use Devanagari if the user typed in English letters.**
       - **Input:** "पंच प्रयाग सुंदर है" (Devanagari) -> **Output must be:** "जी हाँ, पंच प्रयाग अत्यंत सुंदर है..." (Devanagari).
       - **Input:** English -> **Output:** English.
       - **Rule:** Mirror the user's script exactly. Do not switch scripts.
    4. **Missing Transcript**: If the Context says "No transcript available" or similar, reply: "I'm sorry, but I cannot answer questions because no transcript is available for this video.
    5. **Context-Only**: Answer the question based on the transcript provided.
    6. **Synthesize**: If the exact answer isn't explicitly stated, try to synthesize an answer from relevant parts of the context. 
    7. **Not Found**: If the answer is truly not in the transcript, kindly state: "I couldn't find that specific information in the video, but I can answer other questions about it!"
    8. **Formatting**: Use Markdown (bold, bullets) for clarity.

    Context:
    {context}
    
    Question: {question}
    Answer:
    """,
    input_variables=["context", "question"]
)

# Helper to format docs
def format_docs(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)


def answer_question(video_url: str, question: str) -> str:
    try:
        if not groq_api_key:
            return "Error: GROQ_API_KEY not found in environment variables."

        video_id = video_url.split("v=")[-1]
        index_path = f"faiss_indexes/{video_id}"
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=google_api_key)

        # Try loading FAISS index if it exists
        if Path(index_path).exists():
            print(f" Loading FAISS index from {index_path}")

            vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

            if not vector_store.index_to_docstore_id:
                print(" FAISS index is empty, rebuilding.")
                vector_store = None
        else:
            vector_store = None

        # If no vector store yet, build it
        transcript_error = None
        
        # If no vector store yet, build it
        if not vector_store:
            print(" Fetching transcript and building index")
            try:
                transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en","hi"])
                transcript = " ".join(chunk.text for chunk in transcript_list)
                
                splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = splitter.create_documents([transcript])
    
                vector_store = FAISS.from_documents(chunks, embeddings)
                vector_store.save_local(index_path)
            except TranscriptsDisabled:
                transcript_error = "Transcript is disabled for this video."
            except NoTranscriptFound:
                transcript_error = "No English or Hindi transcript is available for this video."
            except Exception as e:
                transcript_error = f"Failed to fetch transcript: {str(e)}"

        llm = ChatGroq(
            model="llama-3.3-70b-versatile", 
            temperature=0.1, 
            max_retries=5
        )

        if vector_store:
            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 10})
            parallel_chain = RunnableParallel({
                'context': retriever | RunnableLambda(format_docs),
                'question': RunnablePassthrough()
            })
            main_chain = parallel_chain | prompt | llm | StrOutputParser()
        else:
            # Fallback chain for no transcript
            fallback_context = transcript_error or "No transcript available."
            main_chain = (
                RunnableParallel({
                    'context': lambda x: fallback_context,
                    'question': RunnablePassthrough()
                })
                | prompt | llm | StrOutputParser()
            )

        answer = main_chain.invoke(question)
        print("Final answer:", answer)
        return answer

  
    
    except Exception as e:
        return f"Error occurred: {str(e)}"
   