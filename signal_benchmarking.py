# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 20:48:17 2025

@author: busin
"""

# signal_benchmarking.py

def score_signal(job):
    score = 0
    if job.get("tech_stack"):
        score += len(job["tech_stack"]) * 1.5
    if job.get("role_tags"):
        score += len(job["role_tags"]) * 1.0
    if job.get("team_tag"):
        score += 1.0
    if job.get("wage_band"):
        score += 2.0
    desc_len = job.get("description_length", 0)
    if desc_len > 100:
        score += 1.0
    elif desc_len > 50:
        score += 0.5
    return round(score, 2)