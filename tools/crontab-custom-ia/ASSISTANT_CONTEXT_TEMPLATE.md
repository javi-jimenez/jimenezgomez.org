---
# ASSISTANT CONTEXT TEMPLATE

This file describes a minimal, machine-friendly format to persist assistant context between sessions.

Frontmatter (YAML) fields (recommended):

- `id`: unique identifier for this context (string)
- `created_at`: ISO8601 timestamp when created
- `updated_at`: ISO8601 timestamp last updated
- `user`: human owner (name)
- `location`: optional location (city, country)
- `purpose`: short description of purpose
- `files_changed`: list of file paths created/modified by the assistant
- `next_steps`: list of next actionable items (short strings)
- `status`: one of `active`, `paused`, `completed`

Body (human-friendly):
- Short chronological log of actions
- Commands to run locally for verification
- Where to look for logs and important files

Example:

---
id: "crontab-custom-ia-2025-12-30"
created_at: "2025-12-30T12:00:00+01:00"
updated_at: "2025-12-30T12:00:00+01:00"
user: "Francisco Javier"
location: "Valencia, España"
purpose: "Local meta-runner for IA editorial jobs and weekly planner"
files_changed:
  - "~/data/crontab-custom-ia/run_cron_meta.sh"
  - "~/data/crontab-custom-ia/jobs/run_weekly_planner.sh"
  - "~/data/crontab-custom-ia/weekly_content_planner.py"
  - "content/posts/2024-02-01-deb-get-winget-linux/index.md"
next_steps:
  - "(opt) set GITHUB_REPOSITORY and GITHUB_TOKEN in ~/.profile to enable issue creation"
  - "review blog draft at content/posts/2025-12-30-assistant-context-standard/index.md"
status: "active"
---

Log:
- 2025-12-30: Created meta-runner + weekly planner; added cron entry; added deb-get article.

Commands:
- Run meta-runner: `/home/user/data/crontab-custom-ia/run_cron_meta.sh`
- View logs: `tail -n 200 ~/data/crontab-custom-ia/logs/cron.log`
