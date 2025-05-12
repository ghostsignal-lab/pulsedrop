import json
import os
from generate import generate_application
from utils import load_bullet_bank
from log_utils import log_application, already_logged


def load_job_feed(feed_path="job_feed.json"):
    with open(feed_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def batch_apply(feed_path="job_feed.json", bullet_bank_path="structured_bullet_bank.json"):
    jobs = load_job_feed(feed_path)
    bullet_bank = load_bullet_bank(bullet_bank_path)
    for job in jobs:
        company = job["company"]
        title= job["title"]
        url = job["url"]
        source = job.get("source","unknown")

        if already_logged(url):
            print(f"Skipping {company} -- already logged.")
            continue
        try:
            resume, cover = generate_application(
                job_desc= job["description"],
                job_title=title,
                company_name=company,
                bullet_bank=bullet_bank
            )
            log_application(
                company=company,
                job_title=title,
                source=source,
                url=url,
                resume_path=resume,
                cover_letter_path=cover,
                status="generated"
            )
            print(f"Applied to {company} -- {title}")
        except Exception as e:
            print(f" Failed on {company} -- {e}")
            log_application(
                company=company,
                job_title=title,
                source=source,
                url=url,
                resume_path="",
                cover_letter_path="",
                status="error",
                notes=str(e)
            )
if __name__=="__main__":
    batch_apply()