from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Prompt Template
prompt = PromptTemplate(
    template="""
    You are a helpful YouTube assistant powered by Google Gemini.
    
    INSTRUCTIONS:
    1. If the user's input is a greeting (e.g., "Hi", "Hello", "Hey"), reply with a warm, short greeting introducing yourself as "YouTube RAG Bot". DO NOT use the provided context for greetings.
    2. For all other questions, answer ONLY based on the provided transcript context below.
    3. If the answer is not in the context, say "I couldn't find the answer in the video transcript."
    4. Format your answer with Markdown (bullet points, bold text) where appropriate for readability.

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
        if not google_api_key:
            return "Error: GOOGLE_API_KEY not found in environment variables."

        video_id = video_url.split("v=")[-1]
        index_path = f"faiss_indexes/{video_id}"
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

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
        if not vector_store:

            print(" Fetching transcript and building index")
            
            try:
                transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
                transcript = " ".join(chunk.text for chunk in transcript_list)
            except TranscriptsDisabled:
                return " Transcript is disabled for this video."
            except NoTranscriptFound:
                return " No English transcript is available for this video."
            except Exception as e:
                return f" Failed to fetch transcript: {str(e)}"

         
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.create_documents([transcript])

            vector_store = FAISS.from_documents(chunks, embeddings)
            vector_store.save_local(index_path)

        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 10})

        parallel_chain = RunnableParallel({
            'context': retriever | RunnableLambda(format_docs),
            'question': RunnablePassthrough()
        })

        llm = ChatGoogleGenerativeAI(
            model="gemini-flash-lite-latest", 
            temperature=0.1, 
            max_retries=5
        )
        main_chain = parallel_chain | prompt | llm | StrOutputParser()

        answer = main_chain.invoke(question)
        print("Final answer:", answer)
        return answer

  
    
    except Exception as e:
        return f"Error occurred: {str(e)}"
   