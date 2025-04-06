"""Script to check if 'AI Spam' label is present on a pull request, and take action."""

import json
import os
from github import Github

context_dict = json.loads(os.getenv("CONTEXT_GITHUB"))
repo_name = context_dict["repository"]
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(repo_name)
pr_number = context_dict["event"]["pull_request"]["number"]
pr = repo.get_pull(number=pr_number)

label_names = [label.name for label in pr.get_labels()]

if "AI Spam" in label_names:
    pr.create_issue_comment(
        "This pull request has been flagged as AI-generated spam and is being automatically closed."
    )

    pr.edit(state="closed")
