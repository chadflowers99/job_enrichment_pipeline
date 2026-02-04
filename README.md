# 🧠 Job Enrichment Pipeline

A suppressor‑aware, modular pipeline for deduplicating, filtering, enriching, and narrating infrastructure‑aligned job data. Built for remote‑first teams and recruiter review.

## 👋 Overview

This project transforms noisy job batches into audit‑safe, narratable datasets. It reflects my engineering philosophy: suppressor‑aware clarity, schema hygiene, and markdown storytelling.

## 🧩 Modules at a Glance (Pipeline Stages)

| Module                 | Pipeline Stage        | Purpose                                                                 | Output                                   |
|------------------------|------------------------|-------------------------------------------------------------------------|-------------------------------------------|
| `deduplication_stub.py` | **Stage 1 — Hygiene**     | Cleans encodings, patches corrupted text, suppresses malformed entries, deduplicates | `deduped_batch.json`, `suppressed_batch.json` |
| `filter_entries.py`     | **Helper Library**        | Role‑tag filters, tech‑stack filters, saturation checks, unfamiliar‑tech suppressor | Used by `benchmark_runner.py` |
| `benchmark_runner.py`   | **Stage 2 — Enrichment**  | Applies filters, scores jobs and platforms, normalizes fields, narrates suppressions | `benchmarked_batch.json` |
| `narrate_batch.py`      | **Stage 3 — Summary**     | Generates batch‑level markdown summary with score buckets and suppression breakdown | `infra_batch_summary.md` |
| `sql_import.py`         | **Stage 4 — Persistence** | Loads enriched data into SQLite for querying and dashboard use          | `jobs.db` |
| `md_exporter.py`        | **Stage 5 — Presentation**| Exports one markdown file per job and platform                          | `job_markdowns/`, `platform_markdowns/` |
| `run_pipeline.py`       | **Orchestrator**          | Runs all pipeline stages in sequence, halting on failure                | Full pipeline output |

🚀 Running the Pipeline  
- Take the role or job description you want to enrich.  
- Use the current rawfeed_batch.json as a template (convert it using AI).  
- Save the updated content into rawfeed_batch.json at the project root.  
- Run:  
    python run_pipeline.py

## 📡 Platform Intelligence Profiles

In addition to job‑level enrichment, the pipeline supports platform‑level intelligence.  
These entries are not scraped from APIs — they are qualitative, suppressor‑aware evaluations of job platforms based on:  
- role density  
- schema consistency  
- tech‑stack transparency  
- suppressor saturation  
- contract hygiene  
- platform behavior and drift patterns  

Each platform is represented as a structured JSON object:

```json
{
  "platform_id": "",
  "name": "",
  "website": "",
  "platform_type": "",
  "infra_role_density": "",
  "tooling_transparency": "",
  "contract_hygiene": "",
  "suppressor_saturation": "",
  "tech_stack_coverage": [],
  "schema_drift_notes": "",
  "ideal_for": [],
  "notes": ""
}
```

Platform profiles allow the pipeline to:  
- benchmark platforms alongside jobs  
- narrate platform‑level suppressions  
- generate markdown summaries for recruiter‑ready review  
- support future agentic workflows (e.g., platform selection, sourcing strategy, noise‑aware job scouting)  

Platform entries live in rawfeed_batch.json alongside job entries and flow through the same enrichment and narration stages.

## 📦 Outputs

- JSON: deduplicated, suppressed, and enriched batches  
- Markdown: recruiter‑friendly summaries and individual entries  
- SQLite: structured querying and dashboard‑ready data  
- All artifacts appear directly in the project directory  

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
