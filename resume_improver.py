def improve_resume(resume_data):

    suggestions = []

    if not resume_data.get("summary"):
        suggestions.append({
            "section": "Professional Summary",
            "suggestion": "Add a short professional summary describing your skills, strengths, and career goal."
        })

    if not resume_data.get("projects"):
        suggestions.append({
            "section": "Projects",
            "suggestion": "Add 2-3 relevant projects and mention the technologies used in each project."
        })

    if not resume_data.get("experience"):
        suggestions.append({
            "section": "Experience",
            "suggestion": "Add internships, hackathons, freelance work, or other practical experience if available."
        })

    if not resume_data.get("soft_skills"):
        suggestions.append({
            "section": "Soft Skills",
            "suggestion": "Add relevant soft skills such as communication, teamwork, problem-solving, or leadership."
        })

    if not resume_data.get("certifications"):
        suggestions.append({
            "section": "Certifications",
            "suggestion": "Add relevant certifications or completed courses."
        })

    if not resume_data.get("achievements"):
        suggestions.append({
            "section": "Achievements",
            "suggestion": "Add academic, technical, hackathon, or other notable achievements if available."
        })

    if not resume_data.get("links"):
        suggestions.append({
            "section": "Professional Links",
            "suggestion": "Add professional links such as GitHub, LinkedIn, or your portfolio."
        })

    if not resume_data.get("skills"):
        suggestions.append({
            "section": "Technical Skills",
            "suggestion": "Add relevant technical skills based on your education and projects."
        })

    return suggestions