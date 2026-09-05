# 🤖 AI Career Assistant

An AI-powered career assistant that combines **Resume Parsing, Semantic Job Matching, and a RAG-based Career Chatbot** into one Streamlit application.

The project uses **Google Gemini** for AI-powered text generation, **Sentence Transformers** for local embeddings, and **FAISS** for semantic similarity search.

---

🚀 Features

### 📄 1. Resume Parsing

Upload a resume in PDF format and the application extracts important information such as:

- Name
- Email
- Phone
- Skills
- Education
- Experience
- Projects

The extracted information is returned as structured JSON using Gemini.

### 🔎 2. Semantic Job Search

The uploaded resume is analyzed to extract the candidate's:

- Skills
- Projects

These details are converted into a semantic query and compared with job descriptions using embeddings and FAISS.

The system returns the most relevant job opportunities based on semantic similarity.

### 💬 3. AI Career Mentor

A RAG-based chatbot that answers career-related questions using a collection of career notes.

The system:

1. Loads career documents
2. Splits them into smaller chunks
3. Converts the chunks into embeddings
4. Stores them in FAISS
5. Retrieves the most relevant chunks for a question
6. Uses Gemini to generate the final answer

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- PyPDF2
- LangChain
- Hugging Face Sentence Transformers
- FAISS
- Python-dotenv

---

## 🧠 Architecture

                    AI Career Assistant
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        Resume Parser   Semantic Search   RAG Chatbot
              │            │            │
              ▼            ▼            ▼
           Gemini       Embeddings      Career Notes
                           │            │
                           ▼            ▼
                         FAISS        FAISS
              │            │            │
              └────────────┼────────────┘
                           ▼
                    Streamlit Interface



## 📁 Project Structure

AI_Career_Assistant/
│
├── app.py
├── parse.py
├── Semantic.py
├── rag.py
├── rag_langchain.py
├── requirements.txt
├── .gitignore
│
└── data/
    └── career_notes/


## ⚙️ Installation

  1. Clone the repository
      git clone <YOUR_GITHUB_REPOSITORY_URL>
      cd AI_Career_Assistant
  2. Create a virtual environment
      python -m venv venv

  Activate it on Windows:
      venv\Scripts\activate
  
  3.Install dependencies
      pip install -r requirements.txt


## 🔑 Gemini API Key

Create a .env file in the project root:
    GEMINI_API_KEY=your_api_key_here


## ▶️ Run the Application

Start the Streamlit application with:
  streamlit run app.py


## 🔍 How Semantic Search Works
Resume PDF
    →
Resume Parser
    →
Skills + Projects
    →
Query Creation
    →
Sentence Transformer Embeddings
    →
FAISS Similarity Search
    →
Top Matching Jobs


## 💬 How RAG Chatbot Works
Career Notes
     →
Document Loading
     →
Text Chunking
     →
Local Embeddings
     →
FAISS Vector Store
     →
Relevant Chunks
     →
Gemini
     →
Final Answer
