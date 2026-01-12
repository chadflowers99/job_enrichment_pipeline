# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 18:40:56 2025

@author: busin
"""

# platform_runner.py

KNOWN_TECH = [
    "Python", "Docker", "Terraform", "Kubernetes", "SQL",
    "Linux", "CI/CD", "Monitoring", "CloudFormation", "Ansible",
    "AWS", "PostgreSQL", "Grafana", "OpenTelemetry", "ECS", "EKS"
]

def score_platform(platform, known_tech=None):
    if known_tech is None:
        known_tech = KNOWN_TECH

    coverage = platform.get("tech_stack_coverage", [])
    overlap = [tech for tech in coverage if tech in known_tech]
    saturation = platform.get("suppressor_saturation", "unknown")
    hygiene = platform.get("contract_hygiene", "unknown")
    transparency = platform.get("tooling_transparency", "unknown")

    score = 0
    score += len(overlap) * 0.5
    score += {"low": 2, "medium": 1, "high": 0}.get(saturation, 0)
    score += {"high": 2, "medium": 1, "low": 0}.get(hygiene, 0)
    score += {"high": 2, "medium": 1, "low": 0}.get(transparency, 0)

    platform["platform_score"] = round(score, 2)
    return platform

def reorder_platform(platform):
    return {
        "platform_id": platform.get("platform_id"),
        "platform_score": platform.get("platform_score"),
        "name": platform.get("name"),
        "website": platform.get("website"),
        "platform_type": platform.get("platform_type"),
        "infra_role_density": platform.get("infra_role_density"),
        "tooling_transparency": platform.get("tooling_transparency"),
        "contract_hygiene": platform.get("contract_hygiene"),
        "suppressor_saturation": platform.get("suppressor_saturation"),
        "tech_stack_coverage": platform.get("tech_stack_coverage"),
        "ideal_for": platform.get("ideal_for"),
        "schema_drift_notes": platform.get("schema_drift_notes"),
        "notes": platform.get("notes")
    }