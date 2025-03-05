from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")  # Free & widely used
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def CreateVectorDbFromYoutube(video_url: str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    texts = [chunk.page_content for chunk in docs]  # Extract text content

    # ✅ Use FAISS.from_texts() instead of FAISS.from_embeddings()
    db = FAISS.from_texts(texts, embeddings_model)  

    return db

def GetResponseFromQuery(db, query, k=4): 
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])
    
    llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7
    )

    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are a helpful YouTube assistant that can answer questions about
        videos
        based on the video's transcript.
         
        Answer the following question: {question}
        By searching the following video transcript: {docs}
          
        Only use the factual information from the transcript to answer the questions.
        
        If you feel like you don't have enough information to answer the question,
        say "I don't know".
          
        Your answers should be detailed.
        """
    )
    name_chain = prompt | llm
    response = name_chain.invoke({"question": query, "docs": docs_page_content}).content
    response = response.replace("\n", "")
    return response