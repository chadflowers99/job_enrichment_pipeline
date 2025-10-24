# 🧠 Job Enrichment Pipeline

A suppressor-aware, modular pipeline for deduplicating, filtering, enriching, and narrating infrastructure-aligned job data. Built for remote-first teams and recruiter review.

## 👋 Overview

This project transforms noisy job batches into audit-safe, narratable datasets. It reflects my engineering philosophy: suppressor-aware clarity, schema hygiene, and markdown storytelling.

## 🧩 Modules at a Glance

| Module               | Purpose                                                       | Output                          |
|----------------------|---------------------------------------------------------------|----------------------------------|
| `deduplication_stub.py` | Cleans encodings, suppresses malformed entries, deduplicates | `deduped_batch.json`, `suppressed_batch.json` |
| `filter_entries.py`     | Helper functions for role/tech filtering, saturation checks, and suppressor logic | Used by `benchmark_runner.py` |
| `benchmark_runner.py`   | Orchestrates enrichment: scoring, filtering, narration       | `benchmarked_batch.json`        |
| `narrate_batch.py`      | Generates markdown summaries with signal buckets             | `infra_batch_summary.md`        |
| `sql_import.py`         | Imports enriched data into SQLite                            | `jobs.db`                       |
| `md_exporter.py`        | Exports markdown slices for each job and platform            | `job_markdowns/`, `platform_markdowns/` |

## 📦 Outputs

- JSON: deduplicated, suppressed, and enriched batches
- Markdown: recruiter-friendly summaries and individual entries
- SQLite: structured querying and dashboard-ready data

## 🧼 Design Philosophy

- Suppressor-aware filtering and narration
- Modular batch hygiene and tech fluency benchmarking
- Markdown storytelling for recruiter clarity
- SQLite-backed persistence for audit-safe review

## 🛠️ Tech Stack

- Python · JSON · Markdown · SQLite
- `difflib`, `re`, `datetime`, `os`, `collections`

---

🧠 Built by Chad — diagnostic architect and workflow engineer  
🎯 Modularizing enrichment pipelines for infra-aligned clarity  
📁 GitHub-ready for recruiter review and remote-first roles
