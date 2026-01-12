# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 21:00:17 2025

@author: busin
"""

# narrate_batch.py

import json
from datetime import datetime
from collections import Counter

# -------------------------------
# 📥 Load Benchmarked Batch
# -------------------------------

def load_batch(path="benchmarked_batch.json"):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Failed to parse JSON from: {path}")
        return []

# -------------------------------
# 📊 Score Distribution Narrator
# -------------------------------

def narrate_score_distribution(jobs):
    bins = {"30+": 0, "20–29": 0, "10–19": 0, "<10": 0}
    for job in jobs:
        score = job.get("signal_score", 0)
        if score >= 30:
            bins["30+"] += 1
        elif score >= 20:
            bins["20–29"] += 1
        elif score >= 10:
            bins["10–19"] += 1
        else:
            bins["<10"] += 1
    return bins

# -------------------------------
# 📉 Suppression Breakdown
# -------------------------------

def narrate_suppressions(jobs):
    suppressed = [j for j in jobs if j.get("suppression_reason")]
    reasons = Counter(j["suppression_reason"] for j in suppressed)
    return suppressed, reasons

# -------------------------------
# 📈 Scoring Utilities
# -------------------------------

def score_jobs(jobs):
    return sorted(jobs, key=lambda j: j.get("signal_score", 0), reverse=True)

def score_platforms(platforms):
    return sorted(platforms, key=lambda p: p.get("platform_score", 0), reverse=True)

# -------------------------------
# 📝 Markdown Summary Writer
# -------------------------------

def write_summary(jobs, platforms, filename="infra_batch_summary.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Infra Batch Summary\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

        f.write("## 📊 Signal Score Distribution\n")
        bins = narrate_score_distribution(jobs)
        for label, count in bins.items():
            f.write(f"- {label}: {count}\n")
        f.write("\n")

        suppressed, reasons = narrate_suppressions(jobs)
        f.write(f"## 🚫 Suppressed Jobs: {len(suppressed)}\n")
        for reason, count in reasons.items():
            f.write(f"- {reason}: {count}\n")
        f.write("\n")

        f.write("## 💼 Top Jobs\n")
        for job in score_jobs(jobs)[:5]:
            f.write(f"- {job.get('title')} at {job.get('company')} → {job.get('signal_score')}\n")
        f.write("\n")

        f.write("## 🧠 Top Platforms\n")
        for p in score_platforms(platforms)[:5]:
            f.write(f"- {p.get('name')} → {p.get('platform_score')}\n")

# -------------------------------
# 🚀 Main Execution
# -------------------------------

def main():
    entries = load_batch()
    if not entries:
        print("⚠️ No entries to summarize.")
        return

    jobs = [e for e in entries if "job_id" in e]
    platforms = [e for e in entries if "platform_id" in e]

    write_summary(jobs, platforms)
    print(f"\n✅ Summary written to infra_batch_summary.md")
    print(f"📊 Jobs: {len(jobs)} | Platforms: {len(platforms)}")

# -------------------------------
# 📦 Exportable Functions
# -------------------------------

__all__ = [
    "load_batch",
    "write_summary",
    "score_jobs",
    "score_platforms",
    "narrate_score_distribution",
    "narrate_suppressions"
]

if __name__ == "__main__":
    main()