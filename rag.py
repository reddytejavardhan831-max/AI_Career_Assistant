import os
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import faiss

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    model_name="gemini-flash-latest"
)

def embed_text(text):
    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content=text,
        output_dimensionality=768
    )

    return result["embedding"]


data_folder = "data/career_notes"
documents = []

for file_name in os.listdir(data_folder):
    if file_name.endswith(".txt"):
        file_path = os.path.join(data_folder,file_name)

        with open(file_path,"r", encoding="utf-8") as file:
            text = file.read()
            documents.append(text)

print("Number of documents:", len(documents))


def chunk_text(text, chunk_size=800 , overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks


all_chunks = []

for document in documents :
    document_chunks = chunk_text(document)
    all_chunks.extend(document_chunks)

print("Number of chunks:" , len(all_chunks))


chunck_embeddings = []
for chunk in all_chunks:
    embedding = embed_text(chunk)
    chunck_embeddings.append(embedding)

chunk_vectors = np.array(chunck_embeddings).astype("float32")
print("Number of embeddings:", len(chunk_vectors))

faiss.normalize_L2(chunk_vectors)

dimension = chunk_vectors.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(chunk_vectors)


def retrieve(query, top_k=3):
    query_embedding = embed_text(query)
    query_vector = np.array([query_embedding]).astype("float32")
    faiss.normalize_L2(query_vector)

    scores , indices = index.search(query_vector, top_k)
    retrieved_chunks = []

    for idx in indices[0]:
        retrieved_chunks.append(all_chunks[idx])

    return retrieved_chunks

def ask(query):
    retrieved_chunks = retrieve(query)
    context = "\n".join(retrieved_chunks)

    prompt = f"""
    You are a helpful AI Career Mentor.

    Answer the user's question using only the information provided in the context below.

    If the answer is not available in the context, say:
    "I don't have enough information in my knowledge base to answer this question."

    CONTEXT:
    {context}

    QUESTION:
    {query}
    """
    response = model.generate_content(prompt)

    return response.text


while True:
    question = input("\nAsk your question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    answer = ask(question)

    print("\nAnswer:")
    print(answer)