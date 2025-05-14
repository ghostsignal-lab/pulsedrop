import json
import re
import os
from tag_extractor.extract import extract_tags_from_text

def load_bullet_bank(path="structured_bullet_bank.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def extract_keywords(text):
    stop_words = {"the", "and", "or", "for","we","are","with","in","on","of"}
    key_words = [word for word in re.findall(r'\b[a-zA-Z0-9+#]{2,}\b',text.lower()) if word not in stop_words]
    return set(key_words)

def create_output_dir(company_name, base_dir="applications"):
    folder = os.path.join(base_dir, company_name.replace(" ","_"))
    os.makedirs(folder, exist_ok=True)
    return folder

def format_skill_list(skills):
        if len(skills)==0:
            return ""
        elif len(skills) == 1:
            return skills[0]
        elif len(skills)==2:
            return f"{skills[0]} and {skills[1]}"
        else:
            return ", ".join(skills[:-1])+ f", and {skills[-1]}"
        
def extract_tags_from_resume(resume_text):
    return extract_tags_from_text(resume_text)

def score_resume_against_job(resume_text, job_text):
    resume_tags = set(extract_tags_from_text(resume_text))
    job_text_lower = job_text.lower()

    matched_tags = {tag for tag in resume_tags if tag.lower().replace('_', ' ') in job_text_lower}
    score = len(matched_tags) / len(resume_tags) if resume_tags else 0.0
    return {
        "resume_tags": sorted(resume_tags),
        "matched_tags": sorted(matched_tags),
        "score": round(score,2)
    }gi