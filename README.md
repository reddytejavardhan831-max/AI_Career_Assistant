#  AI Career Assistant

An AI-powered career assistant that combines **Resume Parsing, Semantic Job Matching, and a RAG-based Career Chatbot** into one Streamlit application.

The project uses **Google Gemini** for AI-powered text generation, **Sentence Transformers** for local embeddings, and **FAISS** for semantic similarity search.

---

 Features :

###  1. Resume Parsing

Upload a resume in PDF format and the application extracts important information such as:

- Name
- Email
- Phone
- Skills
- Education
- Experience
- Projects

The extracted information is returned as structured JSON using Gemini.

### 2. Resume Improvement

The Resume Improvement feature analyzes the extracted resume information and identifies missing sections.

It provides suggestions such as:

- Adding a professional summary
- Adding relevant projects
- Adding internships or practical experience
- Adding soft skills
- Adding certifications
- Adding achievements
- Adding GitHub, LinkedIn, or portfolio links
- Adding relevant technical skills

The system only suggests sections that are missing from the resume.

---

###  3. Semantic Job Search

The uploaded resume is analyzed to extract the candidate's:

- Skills
- Projects

These details are converted into a semantic query and compared with job descriptions using embeddings and FAISS.

The system returns the most relevant job opportunities based on semantic similarity.

###  4. AI Career Mentor

A RAG-based chatbot that answers career-related questions using a collection of career notes.

The system:

1. Loads career documents
2. Splits them into smaller chunks
3. Converts the chunks into embeddings
4. Stores them in FAISS
5. Retrieves the most relevant chunks for a question
6. Uses Gemini to generate the final answer

---

##  Technologies Used

- Python
- Streamlit
- Google Gemini API
- PyPDF2
- LangChain
- Hugging Face Sentence Transformers
- FAISS
- Python-dotenv

---


##  Project Structure

```text
GenAI_Project/
│
├── app.py
├── parse.py
├── resume_improver.py
├── Semantic.py
├── rag.py
├── rag_langchain.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── data/
│   ├── jobs/
│   │   └── job.json
│   │
│   └── career_notes/
│       ├── frontend.txt
│       ├── interview.txt
│       ├── java.txt
│       ├── python.txt
│       ├── AIML.txt
│       ├── DSA.txt
│       ├── Internships.txt
│       ├── JavaScript.txt
│       ├── backend_developer.txt
│       ├── database.txt
│       ├── github.txt
│       └── ...
│
└── faiss_index/
```


##  Installation

  1. Clone the repository
      git clone <YOUR_GITHUB_REPOSITORY_URL>
      cd AI_Career_Assistant
  2. Create a virtual environment
      python -m venv venv
     Activate it on Windows:
         venv\Scripts\activate
  3.Install dependencies
      pip install -r requirements.txt


##  Gemini API Key

Create a .env file in the project root:
    GEMINI_API_KEY=your_api_key_here


##  Run the Application

Start the Streamlit application with:
  streamlit run app.py


## How resume parsing works
Resume PDF
    →
PyPDF2
    →
Extract Resume Text
    →
Gemini
    →
Structured Resume Data
    →
Display Resume Information


## How resume improvement works
Parsed Resume
      →
Check Resume Sections
      →
Identify Missing Sections
      →
Generate Suggestions
      →
Display Improvements


##  How Semantic Search Works
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


##  How RAG Chatbot Works
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
