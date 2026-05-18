#!/usr/bin/env python3
import requests
import csv
import os
from datetime import datetime

REPO = "axamir/Shiftopia"
TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
WEIGHTS = {"activity": 0.4, "approval": 0.3, "creativity": 0.3}

def get_citizens():
    citizens = []
    with open("CITIZENS/INDEX.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            citizens.append(row)
    return citizens

def count_commits(user):
    url = f"https://api.github.com/repos/{REPO}/commits?author={user}&per_page=1"
    resp = requests.get(url, headers=HEADERS)
    # Extract total count from Link header if possible, else fallback
    return 5  # Mock fallback – replace with real logic

def count_positive_votes(user):
    # For now, return a placeholder – real implementation would parse issue comments
    return 3  # Mock

def count_creativity(user):
    # Placeholder – real implementation would count PRs/translations
    return 2  # Mock

def calculate_score(activity, approval, creativity):
    return round(activity*WEIGHTS["activity"] + approval*WEIGHTS["approval"] + creativity*WEIGHTS["creativity"], 2)

def main():
    citizens = get_citizens()
    report = "# Dynamic Valuation Report\n"
    report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "| Citizen | Activity | Approval | Creativity | Score |\n"
    report += "|---------|----------|----------|------------|-------|\n"
    for c in citizens:
        activity = count_commits(c["id"])
        approval = count_positive_votes(c["id"])
        creativity = count_creativity(c["id"])
        score = calculate_score(activity, approval, creativity)
        report += f"| {c['name']} ({c['id']}) | {activity} | {approval} | {creativity} | **{score}** |\n"
    with open("ECONOMY/VALUATION_REPORT.md", "w") as f:
        f.write(report)
    print("✅ گزارش ارزش‌گذاری پویا با موفقیت تولید شد.")

if __name__ == "__main__":
    main()
