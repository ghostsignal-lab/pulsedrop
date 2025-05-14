import csv
import os
from datetime import datetime

LOG_PATH = "application_log.csv"
def log_application(company, job_title, source, url, resume_path, cover_letter_path, status, notes=""):
    row = {
        "timestamp": datetime.now().isoformat(),
        "company": company,
        "job_title": job_title,
        "source": source,
        "url": url,
        "resume_path": resume_path,
        "cover_letter_path": cover_letter_path,
        "status": status,
        "notes": notes
    }
    write_header = not os.path.exists(LOG_PATH)

    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)

def already_logged(url):
    if not os.path.exists(LOG_PATH):
        return False
    with open(LOG_PATH, newline="", encoding="utf-8") as f:
        reader=csv.DictReader(f)
        return any(row["url"]==url for row in reader)