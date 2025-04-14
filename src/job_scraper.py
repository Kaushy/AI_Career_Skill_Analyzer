import requests

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
        print(f"Error: {response.status_code}")
        return []
