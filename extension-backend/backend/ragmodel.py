from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Prompt Template
prompt = PromptTemplate(
    template="""
    You are a helpful assistant.
    Answer ONLY from the provided transcript context in a proper format.
    If the user greets you (e.g. hi, hello), reply warmly before addressing anything else.

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
        video_id = video_url.split("v=")[-1]
        index_path = f"faiss_indexes/{video_id}"
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

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
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
                transcript = " ".join(chunk['text'] for chunk in transcript_list)
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

        llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
        main_chain = parallel_chain | prompt | llm | StrOutputParser()

        answer = main_chain.invoke(question)
        print("Final answer:", answer)
        return answer

  
    
    except Exception as e:
        return f"Error occurred: {str(e)}"
   