import google.generativeai as genai
import numpy as np
import faiss
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

jobs = [
    {
        "role": "Java Backend Developer",
        "skills": "Java, Spring Boot, SQL, REST API"
    },
    {
        "role": "Frontend Developer",
        "skills": "HTML, CSS, JavaScript, React"
    },
    {
        "role": "Python Developer",
        "skills": "Python, Django, Flask, SQL"
    },
    {
        "role": "Data Analyst",
        "skills": "Python, SQL, Excel, Power BI"
    },
    {
        "role": "Machine Learning Engineer",
        "skills": "Python, Machine Learning, TensorFlow, Deep Learning"
    }
]

job_texts = []

for job in jobs:                # TO convert into text
    text = f"""
        Role : {job['role']},
        Required Skills : {job['skills']}
    """
    job_texts.append(text)


def embed(text):                # converts text into embeddings
    result = genai.embed_content(
        model = "models/gemini-embedding-001",
        content = text,
        output_dimensionality = 768
    )

    return result["embedding"]


job_embeddings = []

for text in job_texts:          #to call function 'embed' for conversion
    embedding = embed(text)
    job_embeddings.append(embedding)

job_vectors = np.array(job_embeddings).astype("float32")        # converts into numpy 
faiss.normalize_L2(job_vectors)         # normalizes the vectors


dim = job_vectors.shape[1]          #finds out the size of the embedding i.e 768
index = faiss.IndexFlatIP(dim)      #index is used to store the vectors of size 'dim'
index.add(job_vectors)

def find_matching_jobs(query, top_k=3):     # used to find out top 3 jobs
    query_embedding = embed(query)

    query_vector = np.array([query_embedding]).astype("float32")

    faiss.normalize_L2(query_vector)

    scores, indices = index.search(query_vector, top_k)

    matching_jobs = []

    for score, idx in zip(scores[0], indices[0]):
        job = jobs[idx]

        matching_jobs.append({
            "role": job["role"],
            "skills": job["skills"],
            "similarity_score": float(score)
        })

    return matching_jobs