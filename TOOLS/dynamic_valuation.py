#!/usr/bin/env python3
"""
Dynamic Valuation Tool for Shiftopia
Computes contribution scores for citizens based on activity, approval, and creativity.
Usage: python3 TOOLS/dynamic_valuation.py
"""

import os
import csv
from datetime import datetime

WEIGHTS = {"activity": 0.4, "approval": 0.3, "creativity": 0.3}

def count_github_activity(citizen_handle):
    return 5  # mock

def count_approval_score(citizen_handle):
    return 3  # mock

def count_creativity_score(citizen_handle):
    return 2  # mock

def calculate_score(activity, approval, creativity):
    total = (activity * WEIGHTS["activity"] + approval * WEIGHTS["approval"] + creativity * WEIGHTS["creativity"])
    return round(total, 2)

def main():
    citizens_file = "CITIZENS/INDEX.csv"
    if not os.path.exists(citizens_file):
        print("Error: CITIZENS/INDEX.csv not found.")
        return
    print("=== Shiftopia Dynamic Valuation Report ===\n")
    with open(citizens_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            citizen_id = row["id"]
            name = row["name"]
            activity = count_github_activity(citizen_id)
            approval = count_approval_score(citizen_id)
            creativity = count_creativity_score(citizen_id)
            score = calculate_score(activity, approval, creativity)
            print(f"Citizen: {name} ({citizen_id})")
            print(f"  Activity: {activity} (x{WEIGHTS['activity']})")
            print(f"  Approval: {approval} (x{WEIGHTS['approval']})")
            print(f"  Creativity: {creativity} (x{WEIGHTS['creativity']})")
            print(f"  **Total Contribution Score: {score}**\n")
    print("Note: Scores use mock data. Integrate GitHub API for real metrics.")
    print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
