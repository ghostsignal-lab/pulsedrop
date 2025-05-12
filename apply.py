import argparse
import json
from generate import generate_application
from utils import load_bullet_bank

def main():
    parser = argparse.ArgumentParser(description="Generate a resume and cover letter for a job description.")
    parser.add_argument("jd_path", help="Path to job description text file")
    parser.add_argument("--company", required=True, help="Company Name")
    parser.add_argument("--title", required=True, help="Job Title")
    parser.add_argument("--bank", default="structured_bullet_bank.json", help="Path to bullet bank JSON")
    args = parser.parse_args()

    with open(args.jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    with open(args.bank, "r", encoding="utf-8") as f:
        bullet_bank = json.load(f)
    
    resume, cover = generate_application(
        job_desc=jd_text,
        job_title=args.title,
        company_name=args.company,
        bullet_bank=bullet_bank
    )
    print(f"Resume generate: {resume}")
    print(f"Cover letter generated: {cover}")

if __name__ == "__main__":
    main()