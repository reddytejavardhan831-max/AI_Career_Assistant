import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

#embeddings = GoogleGenerativeAIEmbeddings(
#   model="models/gemini-embedding-001",
#    google_api_key=api_key
#)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

loader = DirectoryLoader(
    "data/career_notes",
    glob="*.txt",
    loader_cls=TextLoader
)

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 700,
    chunk_overlap = 100
)
chunks = text_splitter.split_documents(documents)

def get_retriever():
    index_path = "faiss_index"

    if os.path.exists(index_path):
        vector_store = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        vector_store = FAISS.from_documents(
            chunks,
            embeddings
        )

        vector_store.save_local(index_path)

    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )


llm = ChatGoogleGenerativeAI(
    model ="gemini-3.5-flash-lite",
    google_api_key = api_key
)



def ask_rag(query):
    retriever = get_retriever()
    retrieved_docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    prompt = f"""
    Answer the question using only the following context.

    CONTEXT:
    {context}

    QUESTION:
    {query}
    """

    response = llm.invoke(prompt)

    return response.content[0]["text"]