# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 18:41:47 2025

@author: busin
"""

# sql_import.py

import sqlite3
import json
import re

# 🧼 Text Hygiene Utilities
def normalize_utf8(text):
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
    return patch_corrupted_chars(normalize_utf8(text))

def clean_job(job):
    for key, value in job.items():
        if isinstance(value, str):
            job[key] = clean_text(value)
    job["tech_stack"] = [clean_text(t) for t in job.get("tech_stack", [])]
    job["role_tags"] = [clean_text(r) for r in job.get("role_tags", [])]
    return job

# 🧠 SQLite Setup
def create_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        signal_score REAL,
        title TEXT,
        company TEXT,
        location TEXT,
        wage_band TEXT,
        source TEXT,
        suppression_reason TEXT,
        date_posted TEXT,
        days_listed INTEGER,
        tech_stack TEXT,
        role_tags TEXT,
        description_length INTEGER,
        link_count INTEGER,
        batch_stage TEXT,
        notes TEXT
    )
    """)

def create_platform_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platforms (
        platform_id TEXT PRIMARY KEY,
        name TEXT,
        website TEXT,
        platform_type TEXT,
        infra_role_density TEXT,
        tooling_transparency TEXT,
        contract_hygiene TEXT,
        suppressor_saturation TEXT,
        tech_stack_coverage TEXT,
        schema_drift_notes TEXT,
        batch_integrity_score REAL,
        ideal_for TEXT,
        notes TEXT
    )
    """)

def insert_job(cursor, job):
    cursor.execute("""
    INSERT OR REPLACE INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job.get("job_id"),
        job.get("signal_score"),
        job.get("title"),
        job.get("company"),
        job.get("location"),
        job.get("wage_band"),
        job.get("source"),
        job.get("suppression_reason"),
        job.get("date_posted"),
        job.get("days_listed"),
        ", ".join(job.get("tech_stack", [])),
        ", ".join(job.get("role_tags", [])),
        job.get("description_length"),
        job.get("link_count"),
        job.get("batch_stage"),  # ✅ Add this line
        job.get("notes")
    ))

def insert_platform(cursor, platform):
    tech_stack = platform.get("tech_stack_coverage")
    if not isinstance(tech_stack, list):
        tech_stack = []

    ideal_for = platform.get("ideal_for")
    if not isinstance(ideal_for, list):
        ideal_for = []

    cursor.execute("""
    INSERT OR REPLACE INTO platforms VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        platform.get("platform_id"),
        platform.get("name"),
        platform.get("website"),
        platform.get("platform_type"),
        platform.get("infra_role_density"),
        platform.get("tooling_transparency"),
        platform.get("contract_hygiene"),
        platform.get("suppressor_saturation"),
        ", ".join(tech_stack),
        platform.get("schema_drift_notes"),
        platform.get("batch_integrity_score"),
        ", ".join(ideal_for),
        platform.get("notes")
    ))

# 🚀 Main Execution
if __name__ == "__main__":
    with open("benchmarked_batch.json", encoding="utf-8") as f:
        jobs = json.load(f)

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    create_table(cursor)
    create_platform_table(cursor)

    cursor.execute("DELETE FROM jobs")
    cursor.execute("DELETE FROM platforms")
    
    job_count = 0
    platform_count = 0
    
    for entry in jobs:
        if "platform_id" in entry:
            try:
                insert_platform(cursor, entry)
                platform_count += 1
            except Exception as e:
                print(f"❌ Failed to insert platform {entry.get('platform_id')}: {e}")
        else:
            clean_job(entry)
            insert_job(cursor, entry)
            job_count += 1
    
    conn.commit()
    conn.execute("VACUUM")
    conn.close()
    print(f"✅ Imported {job_count} jobs and {platform_count} platforms into jobs.db")