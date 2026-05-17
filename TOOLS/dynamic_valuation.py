#!/usr/bin/env python3
"""
Dynamic Valuation Tool for Shiftopia
Fetches real data from GitHub API to compute contribution scores.
Requires `gh` CLI and GITHUB_TOKEN with appropriate scopes.
Usage: python3 TOOLS/dynamic_valuation.py
"""

import subprocess
import json
import csv
import os
from datetime import datetime

REPO = "axamir/Shiftopia"
WEIGHTS = {"activity": 0.4, "approval": 0.3, "creativity": 0.3}

def run_gh_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {cmd}")
        return []
    return json.loads(result.stdout)

def get_citizens():
    citizens = []
    with open("CITIZENS/INDEX.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            citizens.append(row)
    return citizens

def count_commits(user):
    # Count commits by the user in the repo (simplified)
    data = run_gh_command(f"gh api repos/{REPO}/commits?author={user}&per_page=100")
    return len(data)

def count_positive_votes(user):
    # Search issues/comments where user's comment was positive (approve, +1, 👍)
    # For simplicity, count issues where user commented with "approve" or "موافق"
    query = f"repo:{REPO} commenter:{user} approve OR موافق"
    data = run_gh_command(f'gh api search/issues --q "{query}"')
    return data.get("total_count", 0)

def count_creativity(user):
    # Count PRs created by user (translations, new veils, new jobs)
    data = run_gh_command(f"gh api repos/{REPO}/pulls?state=all&creator={user}&per_page=100")
    return len(data)

def calculate_score(activity, approval, creativity):
    total = (activity * WEIGHTS["activity"] +
             approval * WEIGHTS["approval"] +
             creativity * WEIGHTS["creativity"])
    return round(total, 2)

def main():
    citizens = get_citizens()
    report_lines = []
    report_lines.append("# Dynamic Valuation Report\n")
    report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("| Citizen | Activity | Approval | Creativity | Score |\n")
    report_lines.append("|---------|----------|----------|------------|-------|\n")
    for c in citizens:
        user_id = c["id"]
        activity = count_commits(user_id)
        approval = count_positive_votes(user_id)
        creativity = count_creativity(user_id)
        score = calculate_score(activity, approval, creativity)
        report_lines.append(f"| {c['name']} ({user_id}) | {activity} | {approval} | {creativity} | **{score}** |\n")
    with open("ECONOMY/VALUATION_REPORT.md", "w") as f:
        f.writelines(report_lines)
    print("✅ Valuation report written to ECONOMY/VALUATION_REPORT.md")

if __name__ == "__main__":
    main()
