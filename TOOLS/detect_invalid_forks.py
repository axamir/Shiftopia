#!/usr/bin/env python3
import requests
import os
from datetime import datetime

REPO_OWNER = "axamir"
REPO_NAME = "Shiftopia"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def get_forks():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/forks?per_page=100"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []
    return response.json()

def check_chain_of_consent(fork_full_name):
    # Check if CHAIN/GENESIS.md exists and has not been tampered
    url = f"https://raw.githubusercontent.com/{fork_full_name}/main/CHAIN/GENESIS.md"
    try:
        r = requests.get(url, timeout=10)
        return r.status_code == 200 and "Genesis Block" in r.text
    except:
        return False

def main():
    forks = get_forks()
    invalid = []
    for fork in forks:
        full_name = fork["full_name"]
        if not check_chain_of_consent(full_name):
            invalid.append(full_name)
    # Update FORKS.md
    with open("FORKS.md", "r") as f:
        existing = f.read()
    new_entry = f"| {datetime.now().strftime('%Y-%m-%d')} | {', '.join(invalid)} | Missing or altered CHAIN/ | Flagged |\n"
    if invalid:
        # Append to the table (simple)
        with open("FORKS.md", "a") as f:
            f.write(new_entry)
    else:
        print("No invalid forks detected.")

if __name__ == "__main__":
    main()
