# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 17:52:07 2025

@author: busin
"""

# md_exporter.py

import json
import os

# -------------------------------
# 📥 Load Benchmarked Batch
# -------------------------------

with open("benchmarked_batch.json", encoding="utf-8") as f:
    entries = json.load(f)

# -------------------------------
# 🗂️ Create Output Folders
# -------------------------------

os.makedirs("job_markdowns", exist_ok=True)
os.makedirs("platform_markdowns", exist_ok=True)

# -------------------------------
# 🧼 Filename Sanitizer
# -------------------------------

def safe_filename(name):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in str(name))

# -------------------------------
# 🧼 Notes Cleaner
# -------------------------------

def clean_notes(text):
    if not isinstance(text, str): return "None"
    return text.strip() or "None"

# -------------------------------
# 📝 Markdown Templates
# -------------------------------

def job_to_md(job):
    return f"""# {job.get('title', 'Untitled Job')}
**Job ID:** {job.get('job_id', 'N/A')}    
**Company:** {job.get('company', 'Unknown')}  
**Location:** {job.get('location', 'N/A')}  
**Signal Score:** {job.get('signal_score', 'N/A')}
**Batch Stage:** {job.get('batch_stage', 'N/A')}    
**Wage Band:** {job.get('wage_band', 'N/A')}  
**Date Posted:** {job.get('date_posted', 'N/A')}  
**Days Listed:** {job.get('days_listed', 'N/A')}  
**Suppression Reason:** {job.get('suppression_reason', 'None')}  

---

## 🧠 Role Tags  
{', '.join(job.get('role_tags', [])) or 'None'}

## ⚙️ Tech Stack  
{', '.join(job.get('tech_stack', [])) or 'None'}

## 📝 Notes  
{clean_notes(job.get('notes'))}
"""

def platform_to_md(p):
    tech_stack = p.get("tech_stack_coverage", [])
    ideal_for = p.get("ideal_for", [])

    return f"""# {p.get('name', 'Unnamed Platform')}
**Platform ID:** {p.get('platform_id', 'N/A')}    
**Type:** {p.get('platform_type', 'Unknown')}  
**Website:** {p.get('website', 'N/A')}  
**Suppressor Saturation:** {p.get('suppressor_saturation', 'N/A')}  
**Contract Hygiene:** {p.get('contract_hygiene', 'N/A')}  
**Tooling Transparency:** {p.get('tooling_transparency', 'N/A')}  
**Batch Integrity Score:** {p.get('batch_integrity_score', 'N/A')}  
**Platform Score:** {p.get('platform_score', 'N/A')}  

---

## ⚙️ Tech Stack Coverage  
{', '.join(tech_stack) or 'None'}

## 🧠 Ideal For  
{', '.join(ideal_for) or 'None'}

## 📝 Notes  
{clean_notes(p.get('notes'))}
"""

# -------------------------------
# 🧾 Export Markdown Files
# -------------------------------

job_count = 0
platform_count = 0

for entry in entries:
    if "platform_id" in entry:
        filename = f"platform_markdowns/{safe_filename(entry['platform_id'])}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(platform_to_md(entry))
        platform_count += 1
    elif "job_id" in entry:
        filename = f"job_markdowns/{safe_filename(entry['job_id'])}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(job_to_md(entry))
        job_count += 1

# -------------------------------
# ✅ Summary
# -------------------------------

print(f"✅ Exported {job_count} job listings to job_markdowns/")
print(f"✅ Exported {platform_count} platform benchmarks to platform_markdowns/")
print(f"📊 Total entries processed: {len(entries)}")