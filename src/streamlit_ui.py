import streamlit as st
import os
from resume_parser import extract_text_from_pdf, extract_skills
from job_matcher import run_career_path_analysis
import requests

# ----------- Job Fetch Function ------------
def fetch_job_descriptions(skill, location="Chennai"):
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": f"{skill} developer",
        "page": "1",
        "num_pages": "1",
        "location": location
    }
    headers = {
        "X-RapidAPI-Key": "53b7d59eebmsha0a39088400080fp1c2942jsnab4238558ef2",  # API KEY
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        job_descriptions = []
        for job in data.get("data", []):
            job_descriptions.append({
                "job_title": job.get("job_title"),
                "company": job.get("employer_name"),
                "location": job.get("job_city"),
                "description": job.get("job_description"),
                "link": job.get("job_apply_link")
            })
        return job_descriptions
    else:
        return []

# ----------- Streamlit App Starts ------------
st.set_page_config(page_title="AI Career Skill Analyzer", layout="wide")
st.title("🧠 AI Career Skill Analyzer")
st.markdown("Upload your resume to discover matching job roles and skills to improve!")

uploaded_file = st.file_uploader("📤 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    if not os.path.exists("resumes"):
        os.makedirs("resumes")

    resume_path = os.path.join("resumes", uploaded_file.name)
    with open(resume_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ Resume uploaded successfully!")
    st.write(f"📁 File saved at: {resume_path}")

    st.header("🔍 Analyzing Your Resume...")
    resume_text = extract_text_from_pdf(resume_path)
    skills = extract_skills(resume_text)
    st.subheader("✅ Extracted Skills:")
    st.write(skills)

    if skills:
        all_jobs = []
        for skill in skills:
            st.subheader(f"🌐 Job Listings for: {skill}")
            job_listings = fetch_job_descriptions(skill)
            if job_listings:
                all_jobs.extend(job_listings)
                for job in job_listings:
                    st.markdown(f"**{job['job_title']}** at {job['company']} ({job['location']})")
                    st.markdown(f"{job['description'][:200]}...")
                    st.markdown(f"[Apply Here]({job['link']})")
                    st.markdown("---")
            else:
                st.write("No job listings found.")
