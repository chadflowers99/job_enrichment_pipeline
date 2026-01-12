# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 17:41:08 2025

@author: busin
"""

# filter_entries.py

from collections import Counter

# -------------------------------
# 🛠️ Role Tag Filter (Infra-Aligned)
# -------------------------------

def is_job(entry):
    return "platform_id" not in entry

def is_platform(entry):
    return "platform_id" in entry


def filter_by_role_tag(entries, target_tag="Infrastructure Engineer"):
    return [
        entry for entry in entries
        if is_job(entry) and target_tag in entry.get("role_tags", [])
    ]


# -------------------------------
# ⚙️ Tech Stack Filter (Infra Tools)
# -------------------------------

def filter_by_tech_stack(entries, tech_keywords):
    return [
        entry for entry in entries
        if is_job(entry) and any(tech in entry.get("tech_stack", []) for tech in tech_keywords)
    ]


# -------------------------------
# 📊 Saturation Validator
# -------------------------------

def validate_saturation(entries, tag, threshold=0.8):
    jobs = [e for e in entries if is_job(e)]
    total = len(jobs)
    tag_count = sum(tag in job.get("role_tags", []) for job in jobs)
    return total > 0 and (tag_count / total) >= threshold


# -------------------------------
# 🧠 Familiarity Narrator (Infra Fluency)
# -------------------------------

def narrate_familiarity(entries, known_tech=None):
    if known_tech is None:
        known_tech = ["Python", "Docker", "Terraform", "Kubernetes", "SQL"]

    print("🧠 Familiarity scores:")
    for entry in entries:
        if not is_job(entry):
            continue
        overlap = [tech for tech in entry.get("tech_stack", []) if tech in known_tech]
        print(f" - {entry.get('job_id', 'UNKNOWN')} → overlap: {overlap}")


# -------------------------------
# 🧭 Unfamiliar Tech Suppressor
# -------------------------------

def suppress_unfamiliar(entries, known_tech=None, min_overlap=1):
    if known_tech is None:
        known_tech = ["Python", "Docker", "Terraform", "Kubernetes", "SQL"]

    for entry in entries:
        if not is_job(entry):
            continue
        overlap = [tech for tech in entry.get("tech_stack", []) if tech in known_tech]
        if len(overlap) < min_overlap:
            entry["suppression_reason"] = entry.get("suppression_reason") or "unfamiliar_tech"
    return entries


# -------------------------------
# 🔄 Adjacent Tag Suggestor (Infra Context)
# -------------------------------

def suggest_adjacent_tags(entries, base_tag="Infrastructure Engineer", top_n=5):
    tag_counts = Counter(
        tag for entry in entries if is_job(entry) for tag in entry.get("role_tags", [])
    )
    adjacent_tags = [
        tag for tag, count in tag_counts.items()
        if tag != base_tag and count >= 3
    ]
    return adjacent_tags[:top_n]