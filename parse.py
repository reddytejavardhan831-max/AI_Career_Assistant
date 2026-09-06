import PyPDF2       # used to read pdfs
import os           # used to retrieve API key from env and interact with files
import json         # for JSON format
import typing_extensions as typing      # used to define structure of data
from dotenv import load_dotenv          # loads the data from env file
import google.generativeai as genai


load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(          # creating a gemini model
    model_name="gemini-flash-latest",
    system_instruction="You are a helpful AI assistant."
)

class Resume(typing.TypedDict):     # defining the structure of output
    name: str
    email: str
    phone: str
    skills: list[str]
    education: list[str]
    experience: list[str]
    projects: list[str]


# performs parsing of resume
def parse_resume(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf_reader.pages:
        resume_text += page.extract_text()

    prompt = f"""
    Extract the following details from this resume:

    - name
    - email
    - phone
    - skills
    - education
    - experience
    - projects

    Return all the information according to the provided JSON schema.

    If any information is not available in the resume, use null for a single value
    and an empty list [] for a list of values.

    Do not invent information that is not present in the resume.

    RESUME:
    {resume_text}

    JSON:
    """

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=Resume,
            temperature=0.1
        )
    )
    
    resume_data = json.loads(response.text)  # converting JSON to python

    expected_keys = [ "name", "email", "phone", "skills", "education", "experience", "projects"]
    for key in expected_keys:
        resume_data.setdefault(key, None)

    return resume_data

