import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader,TextLoader # used to load files
from langchain_text_splitters import RecursiveCharacterTextSplitter         # used to divide large documnets into smaller chunks
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI         # allows langchain to communicate with Gemini
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

#   embeddings = GoogleGenerativeAIEmbeddings(
#       model="models/gemini-embedding-001",
#       google_api_key=api_key
#   )

embeddings = HuggingFaceEmbeddings(         # converts text into embeddings
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

loader = DirectoryLoader(        
    "data/career_notes",    # tells LAngchain to look inside this folder 
    glob="*.txt",           # tells only files end with .txt
    loader_cls=TextLoader   # it is used to read files
)

documents = loader.load()   # loads all the files 

text_splitter = RecursiveCharacterTextSplitter(     # used to convert documents or files into chunks
    chunk_size = 700,
    chunk_overlap = 100
)
chunks = text_splitter.split_documents(documents)   # divides the documents into chunks by using 'text_splitter'

def get_retriever():
    index_path = "faiss_index"          # stores the FAISS index

    # this is used not to create index every time
    if os.path.exists(index_path):      # checks if index exists or not
        vector_store = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True       # used to load locally saved FAISS index
        )
    else:
        vector_store = FAISS.from_documents(
            chunks,
            embeddings
        )

        vector_store.save_local(index_path)     # saves vectore store locally

    return vector_store.as_retriever(       # retireves the most relavent chunks
        search_kwargs={"k": 3}
    )


llm = ChatGoogleGenerativeAI(       # creating LLM (gemini language model)
    model ="gemini-3.5-flash-lite",
    google_api_key = api_key
)



def ask_rag(query):
    retriever = get_retriever()         # stores return value of 'get_retirever'
    retrieved_docs = retriever.invoke(query)    # calls the 'get_retirever' through retriever variable
    context = "\n\n".join(
        doc.page_content for doc in retrieved_docs  # gets the text from every document
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