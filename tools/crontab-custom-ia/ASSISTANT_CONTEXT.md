---
id: "crontab-custom-ia-2025-12-30"
created_at: "2025-12-30T12:00:00+01:00"
updated_at: "2025-12-30T12:00:00+01:00"
user: "Francisco Javier"
location: "Valencia, España"
purpose: "Local meta-runner for IA editorial jobs and weekly planner"
files_changed:
  - "/home/user/data/crontab-custom-ia/run_cron_meta.sh"
  - "/home/user/data/crontab-custom-ia/jobs/run_weekly_planner.sh"
  - "/home/user/data/crontab-custom-ia/weekly_content_planner.py"
  - "/home/user/data/crontab-custom-ia/install_crontab.sh"
  - "/home/user/data/crontab-custom-ia/README.md"
  - "/home/user/data/crontab-custom-ia/OPERATION.md"
  - "/home/user/data/crontab-custom-ia/ASSISTANT_NOTES.md"
  - "content/posts/2024-02-01-deb-get-winget-linux/index.md"
next_steps:
  - "(opt) set GITHUB_REPOSITORY and GITHUB_TOKEN in ~/.profile to enable issue creation"
  - "review blog draft at content/posts/2025-12-30-assistant-context-standard/index.md"
status: "active"
---

Short log:
- 2025-12-30: Created meta-runner, weekly planner and installed crontab entry (Monday 09:00).
- 2025-12-30: Added deb-get article and SVG image; committed and pushed to remote.

Where to look:
- Meta-runner: `/home/user/data/crontab-custom-ia/run_cron_meta.sh`
- Jobs directory: `/home/user/data/crontab-custom-ia/jobs/`
- Planner: `/home/user/data/crontab-custom-ia/weekly_content_planner.py`
- Logs: `/home/user/data/crontab-custom-ia/logs/cron.log`
- Blog draft: `content/posts/2025-12-30-assistant-context-standard/index.md`

How to resume:
1. Source environment with `GITHUB_REPOSITORY` and `GITHUB_TOKEN` if you want GitHub issue creation.
2. Run `python3 ~/data/crontab-custom-ia/weekly_content_planner.py` to test planner.
3. Edit the blog draft (`content/posts/2025-12-30-assistant-context-standard/index.md`) and set `draft: false` to publish.
