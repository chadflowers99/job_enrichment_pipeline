# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 09:32:14 2025

@author: busin
"""

# benchmark_runner.py

import json
from collections import Counter
from filter_entries import (
    filter_by_role_tag,
    filter_by_tech_stack,
    suppress_unfamiliar
)

# -------------------------------
# 🧠 Known Tech Stack
# -------------------------------

KNOWN_TECH = [
    "Python", "Docker", "Terraform", "Kubernetes", "SQL", "Linux", "CI/CD",
    "Monitoring", "CloudFormation", "Ansible", "AWS", "PostgreSQL", "Grafana",
    "OpenTelemetry", "ECS", "EKS"
]

# -------------------------------
# 📊 Platform Scoring
# -------------------------------

def score_platform(platform, known_tech=KNOWN_TECH):
    tech_stack = platform.get("tech_stack_coverage", [])
    overlap = [tech for tech in tech_stack if tech in known_tech]
    platform["platform_score"] = len(overlap)
    return platform

def reorder_platform(platform):
    keys = [
        "platform_id", "name", "platform_type", "website", "tech_stack_coverage",
        "ideal_for", "contract_hygiene", "tooling_transparency", "suppressor_saturation",
        "batch_integrity_score", "platform_score", "notes"
    ]
    return {k: platform.get(k) for k in keys}

# -------------------------------
# 📈 Job Scoring
# -------------------------------

def score_signal(job, known_tech=KNOWN_TECH):
    tech_stack = job.get("tech_stack", [])
    description_length = job.get("description_length", 0)
    link_count = job.get("link_count", 0)
    role_tags = job.get("role_tags", [])
    wage_band = job.get("wage_band", "")
    raw_days = job.get("days_listed", 0)
    days_listed = raw_days if isinstance(raw_days, (int, float)) else 0

    tech_score = len([t for t in tech_stack if t in known_tech]) * 1.5
    desc_score = min(description_length, 5000) * 0.01
    link_score = min(link_count, 10) * 1.5
    role_score = 10 if "Infrastructure Engineering" in role_tags else 0
    wage_score = 5 if wage_band and "100k" in wage_band.lower() else 0
    recency_penalty = max(0.0, (days_listed - 30) * 0.2)

    score = (
        tech_score +
        desc_score +
        link_score +
        role_score +
        wage_score -
        recency_penalty
    )

    return round(score, 2)

def benchmark_jobs(jobs, threshold=5.0):
    for job in jobs:
        job["batch_stage"] = "benchmarked"
        score = score_signal(job)
        job["signal_score"] = score
        if score < threshold:
            job["suppression_reason"] = job.get("suppression_reason") or "low_signal"
    return jobs

def reorder_job(job):
    keys = [
        "job_id", "signal_score", "title", "company", "location", "wage_band", "source",
        "suppression_reason", "date_posted", "days_listed", "level", "tech_stack",
        "role_tags", "description_length", "link_count", "notes"
    ]
    return {k: job.get(k) for k in keys}

# -------------------------------
# 📉 Suppression Narrator
# -------------------------------

def narrate_suppression(jobs, preview=True, verbose=True):
    suppressed = [j for j in jobs if j.get("suppression_reason") and "job_id" in j]
    reasons = Counter(j["suppression_reason"] for j in suppressed)

    if not verbose:
        return

    print(f"\n🛑 Suppressed {len(suppressed)} jobs")
    for reason, count in reasons.items():
        print(f"   • {reason}: {count}")

    if preview and suppressed:
        print("\n🧪 Previewing first 3 suppressed jobs:")
        for j in suppressed[:3]:
            print(f" - {j.get('job_id', 'UNKNOWN')} → reason: {j.get('suppression_reason', 'unspecified')}")

# -------------------------------
# 📦 Batch Processor
# -------------------------------

def process_batch(batch, known_tech=KNOWN_TECH):
    platforms = [entry for entry in batch if entry.get("platform_id")]
    jobs = [entry for entry in batch if not entry.get("platform_id")]

    jobs = filter_by_role_tag(jobs, target_tag="Infrastructure Engineering")
    jobs = filter_by_tech_stack(jobs, tech_keywords=known_tech)
    jobs = suppress_unfamiliar(jobs, known_tech=known_tech, min_overlap=1)

    jobs = benchmark_jobs(jobs)
    platforms = [score_platform(p, known_tech=known_tech) for p in platforms]

    jobs = [reorder_job(j) for j in jobs]
    platforms = [reorder_platform(p) for p in platforms]

    narrate_suppression(jobs)
    return jobs + platforms

# -------------------------------
# 🚀 Main Runner
# -------------------------------

def run_benchmark_pipeline(input_path="deduped_batch.json", output_path="benchmarked_batch.json"):
    try:
        with open(input_path, encoding="utf-8") as f:
            batch = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {input_path}")
        return
    except json.JSONDecodeError:
        print(f"❌ Failed to parse JSON from: {input_path}")
        return

    print(f"\n🔍 Starting with {len(batch)} entries")
    full_batch = process_batch(batch)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(full_batch, f, indent=2)
        print(f"\n✅ Exported {len(full_batch)} entries to {output_path}")
    except Exception as e:
        print(f"❌ Failed to write output: {e}")

# -------------------------------
# 🧪 CLI Entry Point
# -------------------------------

if __name__ == "__main__":
    run_benchmark_pipeline()