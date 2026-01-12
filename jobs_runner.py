# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 18:40:16 2025

@author: busin
"""

# jobs_runner.py

import json
from signal_benchmarking import score_signal
from filter_jobs import (
    filter_by_role_tag,
    filter_by_tech_stack,
    suppress_unfamiliar
)

KNOWN_TECH = [
    "Python", "Docker", "Terraform", "Kubernetes", "SQL",
    "Linux", "CI/CD", "Monitoring", "CloudFormation", "Ansible",
    "AWS", "PostgreSQL", "Grafana", "OpenTelemetry", "ECS", "EKS"
]

def benchmark_jobs(jobs, threshold=3.0):
    for job in jobs:
        score = score_signal(job)
        job["signal_score"] = score
        if score < threshold:
            job["suppression_reason"] = job.get("suppression_reason") or "low_signal"
    return jobs

def reorder_job(job):
    return {
        "job_id": job.get("job_id"),
        "signal_score": job.get("signal_score"),
        "title": job.get("title"),
        "company": job.get("company"),
        "location": job.get("location"),
        "wage_band": job.get("wage_band"),
        "source": job.get("source"),
        "suppression_reason": job.get("suppression_reason"),
        "date_posted": job.get("date_posted"),
        "days_listed": job.get("days_listed"),
        "level": job.get("level"),
        "tech_stack": job.get("tech_stack"),
        "role_tags": job.get("role_tags"),
        "description_length": job.get("description_length"),
        "link_count": job.get("link_count"),
        "notes": job.get("notes")
    }

def narrate_suppression(jobs, preview=True):
    suppressed = [j for j in jobs if j.get("suppression_reason")]
    reasons = {}
    for j in suppressed:
        reason = j["suppression_reason"]
        reasons[reason] = reasons.get(reason, 0) + 1

    print(f"\n🛑 Suppressed {len(suppressed)} jobs")
    for reason, count in reasons.items():
        print(f"   • {reason}: {count}")

    if preview:
        print("\n🧪 Previewing first 3 suppressed jobs:")
        for j in suppressed[:3]:
            job_id = j.get("job_id", "UNKNOWN")
            reason = j.get("suppression_reason", "unspecified")
            print(f" - {job_id} → reason: {reason}")