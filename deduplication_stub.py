# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 09:30:55 2025

@author: busin
"""

# deduplication_stub.py

import json
import re
from collections import Counter
from difflib import SequenceMatcher

# -------------------------------
# 🧼 Text Hygiene Utilities
# -------------------------------

def normalize_encoding(text):
    if not isinstance(text, str):
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

def patch_corrupted_chars(text):
    if not isinstance(text, str):
        return text
    substitutions = {
        r"â€“": "–", r"â€”": "—", r"â€˜": "‘", r"â€™": "’",
        r"â€œ": "“", r"â€": "”", r"â€¦": "…", r"â€": ""
    }
    for pattern, replacement in substitutions.items():
        text = re.sub(pattern, replacement, text)
    return text

def clean_text(text):
    return patch_corrupted_chars(normalize_encoding(text))

# -------------------------------
# 🔁 Deduplication Logic
# -------------------------------

def is_similar(a, b, threshold=0.85):
    if not a or not b:
        return False
    return SequenceMatcher(None, a, b).ratio() > threshold

def suppress_job(job):
    notes = job.get("notes", "")
    length = job.get("description_length", 0)

    if length < 20 or len(notes.strip()) < 20:
        job["suppression_reason"] = "missing_description"
        return True

    return False

def deduplicate_jobs(jobs, similarity_threshold=0.85):
    seen = []
    deduped = []

    for job in jobs:
        # 🧼 Sanitize string fields
        for key, value in job.items():
            if isinstance(value, str):
                job[key] = clean_text(value)

        # 🧪 Skip platform benchmarks
        if "platform_id" in job:
            deduped.append(job)
            continue

        # 🛑 Suppression check
        if suppress_job(job):
            print(f"🛑 {job.get('job_id', 'UNKNOWN')} suppressed → description_length: {job.get('description_length', 0)}")
            continue

        # 🔁 Duplicate check
        job_id = job.get("job_id", "UNKNOWN")
        title = job.get("title", "").lower()
        company = job.get("company", "").lower()
        location = job.get("location", "").lower()
        notes = job.get("notes", "")
        key = (title, company, location)

        is_duplicate = False
        for existing in seen:
            # Prevent suppressing distinct job_ids
            if job_id == existing.get("job_id"):
                continue

            if key == existing["key"]:
                similarity = SequenceMatcher(None, notes, existing["notes"]).ratio()
                if similarity >= similarity_threshold:
                    job["suppression_reason"] = "duplicate"
                    job["duplicate_of"] = existing.get("job_id", "UNKNOWN")
                    job["deduplication_similarity"] = round(similarity, 2)
                    job["deduplication_source"] = "deduplication_stub"
                    job["batch_stage"] = "deduplicated"
                    print(f"🧹 {job_id} suppressed as duplicate → similarity: {similarity:.2f}")
                    is_duplicate = True
                    
                elif similarity >= 0.75:
                    print(f"⚠️ {job_id} borderline similarity ({similarity:.2f}) → not suppressed")
                    break

        if not is_duplicate:
            seen.append({"key": key, "notes": notes, "job_id": job_id})
            deduped.append(job)

    return deduped

# -------------------------------
# 📉 Suppression Narrator
# -------------------------------

def narrate_suppression(jobs, preview=True):
    suppressed = [j for j in jobs if j.get("suppression_reason") and "job_id" in j]
    reasons = Counter(j["suppression_reason"] for j in suppressed)
    duplicate_count = sum(1 for j in jobs if j.get("suppression_reason") == "duplicate")
    print(f"\n🧹 Duplicates suppressed: {duplicate_count}")

    print(f"\n🛑 Suppressed {len(suppressed)} jobs")
    for reason, count in reasons.items():
        print(f"   • {reason}: {count}")

    if preview:
        print("\n🧪 Previewing first 3 suppressed jobs:")
        for j in suppressed[:3]:
            print(f" - {j.get('job_id', 'UNKNOWN')} → reason: {j.get('suppression_reason', 'unspecified')}")

# -------------------------------
# 🚀 Main Execution
# -------------------------------

if __name__ == "__main__":
    with open("rawfeed_batch.json", encoding="utf-8") as f:
        jobs = json.load(f)

    deduped_jobs = deduplicate_jobs(jobs)
    print(f"\n🧼 Deduplicated: {len(jobs)} → {len(deduped_jobs)}")

    narrate_suppression(jobs)

    suppressed_jobs = [j for j in jobs if j.get("suppression_reason")]
    with open("suppressed_batch.json", "w", encoding="utf-8") as f:
        json.dump(suppressed_jobs, f, indent=2)

    with open("deduped_batch.json", "w", encoding="utf-8") as f:
        json.dump(deduped_jobs, f, indent=2)