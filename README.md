# 🧠 Job Enrichment Pipeline

A suppressor‑aware, modular pipeline for deduplicating, filtering, enriching, and narrating infrastructure‑aligned job data. Built for remote‑first teams and recruiter review.

## 👋 Overview

This project transforms noisy job batches into audit‑safe, narratable datasets. It reflects my engineering philosophy: suppressor‑aware clarity, schema hygiene, and markdown storytelling.

## 🧩 Modules at a Glance (Pipeline Stages)

| Module                  | Pipeline Stage         | Purpose                                                                 | Output                                     |
|-------------------------|-------------------------|-------------------------------------------------------------------------|---------------------------------------------|
| deduplication_stub.py   | Stage 1 — Hygiene       | Cleans encodings, patches corrupted text, suppresses malformed entries, deduplicates | deduped_batch.json, suppressed_batch.json |
| filter_entries.py       | Helper Library          | Role‑tag filters, tech‑stack filters, saturation checks, unfamiliar‑tech suppressor | Used by benchmark_runner.py |
| benchmark_runner.py     | Stage 2 — Enrichment    | Applies filters, scores jobs and platforms, normalizes fields, narrates suppressions | benchmarked_batch.json |
| narrate_batch.py        | Stage 3 — Summary       | Generates batch‑level markdown summary with score buckets and suppression breakdown | infra_batch_summary.md |
| sql_import.py           | Stage 4 — Persistence   | Loads enriched data into SQLite for querying and dashboard use          | jobs.db |
| md_exporter.py          | Stage 5 — Presentation  | Exports one markdown file per job and platform                          | job_markdowns/, platform_markdowns/ |
| run_pipeline.py         | Orchestrator            | Runs all pipeline stages in sequence, halting on failure                | Full pipeline output |

## 🚀 Running the Pipeline

- Take the role or job description you want to enrich.
- Use the current `rawfeed_batch.json` as a template (convert it using AI).
- Save the updated content into `rawfeed_batch.json` at the project root.
- Run:

```bash
python run_pipeline.py
```

## 🧱 Job Entry Format (JSON Schema)

Each job entry in `rawfeed_batch.json` follows this structure:

```json
{
  "job_id": "",
  "title": "",
  "company": "",
  "location": "",
  "wage_band": "",
  "source": "",
  "suppression_reason": null,
  "date_posted": null,
  "days_listed": null,
  "level": "",
  "tech_stack": [],
  "role_tags": [],
  "description_length": 0,
  "link_count": 0,
  "notes": ""
}
```

### Field Notes
- **job_id** — unique identifier for the job  
- **wage_band** — optional; used for wage tagging  
- **suppression_reason** — null unless filtered out  
- **tech_stack** — list of technologies extracted or inferred  
- **role_tags** — qualitative tags used for scoring  
- **description_length** — character count of the job description  
- **notes** — qualitative summary used for narration

## 📡 Platform Intelligence Profiles

In addition to job‑level enrichment, the pipeline supports platform‑level intelligence.  
These entries are not scraped from APIs — they are qualitative, suppressor‑aware evaluations of job platforms based on:

- role density
- schema consistency
- tech‑stack transparency
- suppressor saturation
- contract hygiene
- platform behavior and drift patterns

## 🧱 Platform Entry Format (JSON Schema)

Each platform entry in rawfeed_batch.json follows this structure:


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

### Field Notes
- **platform_type** — classification of the platform (job board, talent marketplace, staffing aggregator)
- **infra_role_density** — qualitative measure of how often infra‑aligned roles appear
- **tooling_transparency** — how clearly the platform exposes tech stacks in listings
- **contract_hygiene** — clarity and honesty of contract terms and employment structure
- **suppressor_saturation** — how noisy, spam‑heavy, or low‑signal the platform tends to be
- **ideal_for** — recommended use cases (e.g., early‑career sourcing, infra‑heavy roles, contract‑first markets)
- **schema_drift_notes** — observations about field inconsistencies or platform‑level drift

Platform profiles allow the pipeline to:

- benchmark platforms alongside jobs
- narrate platform‑level suppressions
- generate markdown summaries for recruiter‑ready review
- support future agentic workflows (platform selection, sourcing strategy, noise‑aware job scouting)

Platform entries live in rawfeed_batch.json alongside job entries and flow through the same enrichment and narration stages.

## 🧭 How to Generate Platform Intelligence Profiles

Platform profiles are qualitative evaluations, not scraped data.  
They are created by prompting an AI model to analyze a job platform based on:

- role density
- schema consistency
- tech‑stack transparency
- suppressor saturation
- contract hygiene
- platform behavior and drift patterns

Prompt to generate a new platform entry (shown without code fences):

Generate a Platform Intelligence Profile for <PLATFORM_NAME> using the JSON schema defined in the README. Base your evaluation on qualitative signals such as role density, schema consistency, tech-stack transparency, suppressor saturation, contract hygiene, and platform behavior. Return ONLY valid JSON that matches the schema.

After generating the JSON, paste the platform entry directly into rawfeed_batch.json alongside job entries. The enrichment pipeline will benchmark platforms and jobs together.

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
- difflib, re, datetime, os, collections

---

🧠 Built by Chad — diagnostic architect and workflow engineer  
🎯 Modularizing enrichment pipelines for infra‑aligned clarity  
📁 GitHub‑ready for recruiter review and remote‑first roles
