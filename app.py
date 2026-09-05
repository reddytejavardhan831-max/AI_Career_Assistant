import streamlit as st
from parse import parse_resume
from Semantic import find_matching_jobs
from rag_langchain import ask_rag

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🤖"
)

st.title("AI Career Assistant")
st.write("Choose a task below:")

task = st.selectbox(
    "Select Task",
    [
        "Resume Parsing",
        "Semantic Search",
        "RAG chatbot"
    ]
)

#-----------------------------------------------TASK 1 (Resume Parsing) -------------------------------------------------
if task == "Resume Parsing":
    st.header("Resume Parsing")
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"]
    )

    if uploaded_file is not None:
        resume_data = parse_resume(uploaded_file)

        st.subheader("Parsed Resume Data")
        st.json(resume_data)
    

#-------------------------------TASK 2 (Semantic Search) ----------------------------------------------------
elif task == "Semantic Search":
    st.header("Semantic search")
    uploaded_file = st.file_uploader(
        "Upload your Resume",
        type=["pdf"],
        key="semantic_resume"
    )

    if uploaded_file is not None:
        resume_data = parse_resume(uploaded_file)

        skills = resume_data.get("skills") or []
        projects = resume_data.get("projects") or []

        query = f"""
        Candidate Skills: {", ".join(skills)}
        Projects: {", ".join(projects)}
        """
        matching_jobs = find_matching_jobs(query)
        st.subheader("Top matching jobs:")

        for job in matching_jobs:
            st.write(f"### {job['role']}")
            st.write(f"**Required Skills:** {job['skills']}")
            st.write(
                f"**Similarity Score:** {job['similarity_score']:.4f}"
            )
            st.divider()

# ------------------------------------------ TASK 3 (RAG chatbot) ---------------------------------------------------------

elif task == "RAG chatbot":
    st.header("RAG chatbot")
    query = st.text_input(
        "Ask any questions on career:"
    )

    if query:
        answer = ask_rag(query)
        st.subheader("Answer:")
        st.write(answer)