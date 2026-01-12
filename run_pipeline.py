# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 11:10:50 2025

@author: busin
"""

# run_pipeline.py

import subprocess

steps = [
    ("Deduplication", ["python", "deduplication_stub.py"]),
    ("Benchmarking", ["python", "benchmark_runner.py"]),
    ("Narration", ["python", "narrate_batch.py"]),
    ("SQL Import", ["python", "sql_import.py"]),
    ("Markdown Export", ["python", "md_exporter.py"]),
]

for label, cmd in steps:
    print(f"\n🚀 Running: {label}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ {label} failed. Halting.")
        break