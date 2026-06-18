from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import tempfile

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SKILLS_DB = [
    "Java", "Python", "C++", "Spring Boot", "Spring", "Hibernate",
    "React", "Angular", "Node.js", "JavaScript", "HTML", "CSS",
    "PostgreSQL", "MySQL", "MongoDB", "Redis",
    "REST API", "GraphQL", "Docker", "Kubernetes",
    "AWS", "EC2", "S3", "Lambda", "GCP",
    "Jenkins", "Git", "GitLab CI/CD",
    "Microservices", "Agile", "Material UI", "Bootstrap"
]

MOCK_JOBS = [
    {
        "title": "Java Full Stack Developer",
        "company": "JPMorgan Chase",
        "location": "Plano, TX / Hybrid",
        "required_skills": ["Java", "Spring Boot", "React", "PostgreSQL", "Docker", "AWS"],
        "apply_link": "https://careers.jpmorgan.com/us/en/students/programs/software-engineer-fulltime"
    },
    {
        "title": "Backend Java Developer",
        "company": "Capital One",
        "location": "Remote / USA",
        "required_skills": ["Java", "Spring Boot", "Microservices", "AWS", "Docker", "PostgreSQL"],
        "apply_link": "https://www.capitalonecareers.com/"
    },
    {
        "title": "Software Engineer - Full Stack",
        "company": "Walmart Global Tech",
        "location": "Bentonville, AR",
        "required_skills": ["Java", "React", "Node.js", "REST API", "Kubernetes", "GCP"],
        "apply_link": "https://careers.walmart.com/"
    },
    {
        "title": "React Frontend Developer",
        "company": "Infosys",
        "location": "Remote / USA",
        "required_skills": ["React", "JavaScript", "HTML", "CSS", "Bootstrap"],
        "apply_link": "https://www.infosys.com/careers/"
    },
    {
        "title": "Cloud Software Engineer",
        "company": "Accenture",
        "location": "Kansas City, MO",
        "required_skills": ["AWS", "Docker", "Kubernetes", "Java", "Microservices"],
        "apply_link": "https://www.accenture.com/us-en/careers"
    }
]


def extract_text_from_pdf(file_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_content)
        temp_path = temp_file.name

    reader = PdfReader(temp_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_skills(text):
    found_skills = []
    lower_text = text.lower()

    for skill in SKILLS_DB:
        if skill.lower() in lower_text:
            found_skills.append(skill)

    return sorted(set(found_skills))


def suggest_role(skills):
    skills_lower = [skill.lower() for skill in skills]

    if "java" in skills_lower and "spring boot" in skills_lower and "react" in skills_lower:
        return "Java Full Stack Developer"

    if "java" in skills_lower and "spring boot" in skills_lower:
        return "Java Backend Developer"

    if "python" in skills_lower:
        return "Python Developer"

    if "react" in skills_lower or "angular" in skills_lower:
        return "Frontend Developer"

    return "Software Developer"


def calculate_match_score(candidate_skills, job_skills):
    candidate_set = set(skill.lower() for skill in candidate_skills)
    job_set = set(skill.lower() for skill in job_skills)

    matched = candidate_set.intersection(job_set)

    if len(job_set) == 0:
        return 0, []

    score = round((len(matched) / len(job_set)) * 100)

    matched_skills = [
        skill for skill in job_skills
        if skill.lower() in matched
    ]

    return score, matched_skills


def recommend_jobs(candidate_skills):
    recommended_jobs = []

    for job in MOCK_JOBS:
        score, matched_skills = calculate_match_score(
            candidate_skills,
            job["required_skills"]
        )

        recommended_jobs.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "match_score": score,
            "matched_skills": matched_skills,
            "missing_skills": [
                skill for skill in job["required_skills"]
                if skill not in matched_skills
            ],
            "apply_link": job["apply_link"]
        })

    recommended_jobs.sort(key=lambda job: job["match_score"], reverse=True)

    return recommended_jobs


@app.get("/")
def home():
    return {"message": "AI Resume Job Recommender API is running"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()

    resume_text = extract_text_from_pdf(content)
    skills = extract_skills(resume_text)
    suggested_role = suggest_role(skills)
    recommended_jobs = recommend_jobs(skills)

    return {
        "filename": file.filename,
        "resume_text": resume_text[:3000],
        "skills": skills,
        "suggested_role": suggested_role,
        "recommended_jobs": recommended_jobs
    }