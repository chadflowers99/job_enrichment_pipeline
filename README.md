# 🧠 Job Enrichment Pipeline

A suppressor‑aware, modular pipeline for deduplicating, filtering, enriching, and narrating infrastructure‑aligned job data. Built for remote‑first teams and recruiter review.

## 👋 Overview

This project transforms noisy job batches into audit‑safe, narratable datasets. It reflects my engineering philosophy: suppressor‑aware clarity, schema hygiene, and markdown storytelling.

## 🧩 Modules at a Glance

| Module                 | Purpose                                                                 | Output                                   |
|------------------------|-------------------------------------------------------------------------|-------------------------------------------|
| `deduplication_stub.py` | Cleans encodings, suppresses malformed entries, deduplicates            | `deduped_batch.json`, `suppressed_batch.json` |
| `filter_entries.py`     | Helper functions for role/tech filtering, saturation checks, suppressor logic | Used by `benchmark_runner.py` |
| `benchmark_runner.py`   | Orchestrates enrichment: scoring, filtering, narration                   | `benchmarked_batch.json` |
| `narrate_batch.py`      | Generates markdown summaries with signal buckets                         | `infra_batch_summary.md` |
| `sql_import.py`         | Imports enriched data into SQLite                                        | `jobs.db` |
| `md_exporter.py`        | Exports markdown slices for each job and platform                        | `job_markdowns/`, `platform_markdowns/` |
| `run_pipeline.py`       | Full pipeline runner: loads, filters, enriches, and exports              | `benchmarked_batch.json` |

## 📦 Outputs

- JSON: deduplicated, suppressed, and enriched batches  
- Markdown: recruiter‑friendly summaries and individual entries  
- SQLite: structured querying and dashboard‑ready data  
- All artifacts appear directly in the project directory  
- A small sample batch can be added to `sample_data/` to demonstrate the pipeline without external APIs  

## 🧼 Design Philosophy

- Suppressor‑aware filtering and narration  
- Modular batch hygiene and tech‑fluency benchmarking  
- Markdown storytelling for recruiter clarity  
- SQLite‑backed persistence for audit‑safe review  

## 🧠 Use Cases

- Cleaning and enriching job‑market datasets  
- Producing recruiter‑ready summaries from noisy sources  
- Demonstrating suppressor‑aware filtering and audit‑safe data pipelines  
- Prototyping GenAI‑ready ingestion and enrichment workflows  

## 🔮 Roadmap

- ONET title inference improvements  
- Wage tagging enhancements  
- Multi‑source ingestion (HN, WWR, etc.)  
- Dashboard layer for batch insights  
- Agentic job‑matching workflow  

## 🛠️ Tech Stack

- Python · JSON · Markdown · SQLite  
- `difflib`, `re`, `datetime`, `os`, `collections`  

---

🧠 Built by Chad — diagnostic architect and workflow engineer  
🎯 Modularizing enrichment pipelines for infra‑aligned clarity  
📁 GitHub‑ready for recruiter review and remote‑first roles
