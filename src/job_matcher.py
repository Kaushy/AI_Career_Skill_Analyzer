def run_career_path_analysis(skills, jobs):
    """
    Matches resume skills with job descriptions to find best-fit career paths.

    Args:
        skills (list): Extracted skills from the resume.
        jobs (list): Job listings (dictionaries) scraped from a job portal.

    Returns:
        list: List of job matches with match score, matched and missing skills.
    """
    matches = []

    for job in jobs:
        # ✅ Safely handle missing job description
        jd_text = job.get('job_description', '').lower()
        if not jd_text:
            continue  # Skip if job description is empty

        matched_skills = [skill for skill in skills if skill.lower() in jd_text]
        missing_skills = [skill for skill in skills if skill.lower() not in jd_text]
        match_score = int((len(matched_skills) / len(skills)) * 100) if skills else 0

        matches.append({
            'job_title': job.get('job_title', 'Unknown Title'),
            'company': job.get('company', 'Unknown Company'),
            'location': job.get('location', 'Unknown Location'),
            'match_score': match_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'link': job.get('link', '#')
        })

    # ✅ Sort matches by best match score
    sorted_matches = sorted(matches, key=lambda x: x['match_score'], reverse=True)
    return sorted_matches
