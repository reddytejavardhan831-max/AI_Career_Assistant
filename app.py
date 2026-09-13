import streamlit as st
from parse import parse_resume
from Semantic import find_matching_jobs
from rag_langchain import ask_rag
from resume_improver import improve_resume

st.set_page_config(
    page_title="AI Career Assistant"
)

st.title("AI Career Assistant")
st.write("Choose a task below:")

task = st.selectbox(
    "Select Task",
    [
        "Resume Parsing",
        "Resume Improvement",
        "Semantic Search",
        "RAG chatbot"
    ]
)

#-----------------------------------------------TASK 1 (Resume Parsing) -------------------------------------------------
if task == "Resume Parsing":

    st.header(" Resume Parsing")

    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success("Resume uploaded successfully!")

        if st.button("▶ Start Parsing"):

            with st.spinner("Parsing your resume..."):

                resume_data = parse_resume(uploaded_file)

            st.subheader(" Parsed Resume")

            st.write("### Personal Information")

            st.write(f"**Name:** {resume_data.get('name') or 'Not available'}")

            st.write(f"**Email:** {resume_data.get('email') or 'Not available'}")

            st.write(f"**Phone:** {resume_data.get('phone') or 'Not available'}")


            st.write("###  Skills")

            skills = resume_data.get("skills") or []

            if skills:
                st.write(", ".join(skills))
            else:
                st.write("Not available")


            st.write("###  Education")

            education = resume_data.get("education") or []

            if education:
                for item in education:
                    st.write(f"- {item}")
            else:
                st.write("Not available")


            st.write("###  Experience")

            experience = resume_data.get("experience") or []

            if experience:
                for item in experience:
                    st.write(f"- {item}")
            else:
                st.write("Not available")


            st.write("###  Projects")

            projects = resume_data.get("projects") or []

            if projects:
                for item in projects:
                    st.write(f"- {item}")
            else:
                st.write("Not available")

#----------------------------------------TASK 2 (Resume Improvement) ---------------------------------------
elif task == "Resume Improvement":

    st.header(" Resume Improvement")

    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success("Resume uploaded successfully!")

        if st.button("▶ Analyze Resume"):

            with st.spinner("Analyzing your resume..."):

                resume_data = parse_resume(uploaded_file)

                suggestions = improve_resume(resume_data)

            st.subheader(" Resume Improvement Suggestions")

            if suggestions:

                for item in suggestions:
                    st.write(f"### {item['section']}")
                    st.write(item["suggestion"])

            else:
                st.write(
                    " Your resume contains all the major sections!"
                )

#-------------------------------TASK 3 (Semantic Search) ----------------------------------------------------
elif task == "Semantic Search":

    st.header(" Semantic Job Search")

    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.success("Resume uploaded successfully!")

        if st.button("▶ Start Job Matching"):

            with st.spinner("Analyzing your resume and finding matching jobs..."):

                resume_data = parse_resume(uploaded_file)

                current_skills = resume_data.get("skills") or []
                projects = resume_data.get("projects") or []

                query = f"""
                Candidate Skills: {", ".join(current_skills)}
                Projects: {", ".join(projects)}
                """

                matching_jobs = find_matching_jobs(query)

            st.subheader(" Top Matching Jobs")

            for i, job in enumerate(matching_jobs, 1):

                required_skills = [
                    skill.strip()
                    for skill in job["skills"].split(",")
                ]

                missing_skills = [
                    skill
                    for skill in required_skills
                    if skill.lower() not in [
                        s.lower() for s in current_skills
                    ]
                ]

                st.markdown(f"### {i}. {job['role']}")

                st.write(
                    f"**Current Skills:** "
                    f"{', '.join(current_skills) if current_skills else 'Not available'}"
                )

                st.write(
                    f"**Required Skills:** "
                    f"{job['skills']}"
                )

                st.write(
                    f"**Missing Skills:** "
                    f"{', '.join(missing_skills) if missing_skills else 'None '}"
                )

                st.write(
                    f"**Similarity Score:** "
                    f"{job['similarity_score'] * 100:.2f}%"
                )

                st.divider()

# ------------------------------------------ TASK 4 (RAG chatbot) ---------------------------------------------------------

elif task == "RAG chatbot":

    st.header(" RAG Career Mentor")

    query = st.text_input(
        "Ask a career-related question:"
    )

    if st.button("▶ Get Answer"):

        if query.strip():

            with st.spinner("Thinking..."):

                answer = ask_rag(query)

            st.subheader(" Answer")
            st.write(answer)

        else:
            st.warning("Please enter a question.")