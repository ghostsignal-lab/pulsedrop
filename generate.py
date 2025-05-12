import os
from datetime import datetime
from collections import defaultdict
from utils import extract_keywords, create_output_dir, format_skill_list
import subprocess

def compile_pdf(tex_path):
    folder =os.path.dirname(tex_path)
    file = os.path.basename(tex_path)
    try: 
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", file],
            cwd=folder,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print("PDF compilation failed:", e)

def match_bullets_to_keywords(bullet_bank, job_desc):
    keywords =extract_keywords(job_desc)
    matched = []
    for entry in bullet_bank:
        role = entry["role"]
        org = entry["org"]
        dates = entry["dates"]
        for bullet in entry["bullets"]:
            score = len(set(bullet["tags"]).intersection(keywords))
            if score>0:
                matched.append({
                    "score":score,
                    "text": bullet["text"],
                    "role": role,
                    "org": org,
                    "dates": dates
                })
        return sorted(matched,key=lambda x: x["score"],reverse=True)
    

def generate_application(job_desc: str, job_title: str, company_name: str, bullet_bank: list) -> tuple[str, str]:
    matched_bullets = match_bullets_to_keywords(bullet_bank, job_desc)

    grouped_experience = defaultdict(list)

    for item in matched_bullets:
        key = (item["role"], item["org"], item["dates"])
        grouped_experience[key].append(item["text"])

    experience_sections = []
    for (role, org, dates), bullets in grouped_experience.items():
        section = [
            f"\\textbf{{{role}}} \\hfill \\textit{{{org}}} \\\\",
            f"\\textit{{{dates}}}",
            "\\begin{itemize}"
        ]
        section += [f"   \\item {bullet}" for bullet in bullets]
        section.append("\\end{itemize}\n")
        experience_sections.append("\n".join(section))
    experience_latex_block = "\n\n".join(experience_sections)

    top_skills = ["support","communication","python"]
    skills_sentence = format_skill_list([s.capitalize() for s in top_skills])
    skill_pairs = [f"{top_skills[i].capitalize()}&{top_skills[i+1].capitalize() if i+1< len(top_skills) else ''} \\\\\\\\" for i in range(0, len(top_skills),2)]
    skills_latex_block = "\\\\begin{tabular}{ 1 1 }\\n"+ "\\n".join(skill_pairs) + "\\n\\\\end{tabular}"
    
    latex_template = f"""
\\documentclass[11pt]{{article}}
\\usepackage[margin=0.75in]{{geometry}}
\\usepackage{{enumitem}}
\\usepackage{{titlesec}}
\\usepackage{{hyperref}}
\\usepackage{{parskip}}

\\titleformat{{\\section}}{{\\bfseries\\Large}}{{}}{{0em}}{{}}[\\titlerule]
\\setlist[itemize]{{noitemsep, topsep=0pt}}

\\begin{{document}}

\\begin{{center}}
    {{\\Large \\textbf{{Your Name}}}} \\\\
    City, State \\quad | \\quad youremail@email.com \\quad | \\quad PHO-NUM-BER \\\\
    \\href{{https://github.com/ghostsignal-lab}} 
\\end{{center}}

\\section*{{Objective}}
Technically adept IT support specialist and CS educator with strong instructional, troubleshooting, and system support experience. Seeking to deliver impactful support in a remote-first enviornment by leveraging cross-platform skills and user-first communication.

\\section*{{Skills}}
{skills_latex_block}

\\section*{{Experience}}
{experience_latex_block}

\\section*{{Education}}
\\textbf{{School}} \\\\
Degree \\quad | \\quad Degree, Date

\\section*{{C ertifactions}}
Certs)
\\end{{document}}
"""
    bullets = [b["text"] for b in matched_bullets[:2]]
    bullet_lines = ""
    if len(bullets)>0:
        bullet_lines+= f"- {bullets[0]}\n"
    if len(bullets)>1:
        bullet_lines+= f"- {bullets[1]}\n"
    cover_leter = f"""
Your Name
City, State
email@email.com | PHO-NUM-BER

{datetime.now().strftime('%B %d, %Y')}

Hiring Team
{company_name}

Dear Hiring Team,

I'm writing to express my interest in the {job_title} role at {company_name}. With a strong background in technical support and cross-platform education, I'm confident in my ability to contribute to your team's mission and user first philosophy.set

My work at Tilden Preparatory School and Mount Diablo Unified involved hands-on support and real-time troubleshooting. I bring experience in {skills_sentence}, all of which align with the core needs of this role. 

Some highlights include:
{bullet_lines}

I admire {company_name}'s innovative edge and would be excited to bring my systems mindset and communication skills to your IT operations. I'd welcome the opportunity to discuss how I can support your users and infrastructure goals.set

Sincerely,
Your Name
"""
    folder = create_output_dir(company_name)
    resume_path = os.path.join(folder, "Resume.tex")
    cover_path = os.path.join(folder, "Cover_Letter.txt")
    with open(resume_path, "w") as f:
        f.write(latex_template)
    compile_pdf(resume_path)
    with open(cover_path, "w") as f:
        f.write(cover_leter)
    return resume_path, cover_path