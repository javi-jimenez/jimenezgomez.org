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
```markdown
---
id: "crontab-custom-ia-2025-12-30"
created_at: "2025-12-30T12:00:00+01:00"
updated_at: "2025-12-31T12:00:00+01:00"
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
  - "content/posts/2025-12-30-assistant-context-standard/index.md"
next_steps:
  - "(opt) set GITHUB_REPOSITORY and GITHUB_TOKEN in ~/.profile or ~/.config/crontab-custom-ia/env to enable issue creation"
  - "review and publish blog draft at content/posts/2025-12-30-assistant-context-standard/index.md (set draft:false)"
status: "active"
---

Short log:
- 2025-12-30: Created meta-runner, weekly planner and installed crontab entry (default Monday 09:00).
- 2025-12-30: Añadí el artículo deb-get y la imagen SVG; registro los cambios y los subo al repositorio remoto.
- 2025-12-31: Documented resume instructions and snapshot for future assistants (this file updated).

Where to look:
- Meta-runner: `/home/user/data/crontab-custom-ia/run_cron_meta.sh`
- Jobs directory: `/home/user/data/crontab-custom-ia/jobs/`
- Planner (runtime copy): `/home/user/data/crontab-custom-ia/weekly_content_planner.py`
- Planner (repo backup): `tools/crontab-custom-ia/weekly_content_planner.py`
- Logs (if enabled): `/home/user/data/crontab-custom-ia/logs/cron.log`
- Blog draft: `content/posts/2025-12-30-assistant-context-standard/index.md`

How to resume (step-by-step):
1. Ensure the local env file exists and is secure:
  - Path: `~/.config/crontab-custom-ia/env`
  - Permissions: `chmod 600 ~/.config/crontab-custom-ia/env`
  - Required variables: `GITHUB_TOKEN`, `GITHUB_REPOSITORY` (optional: `MAINTAINER_EMAIL`).
2. Source the env (or export the variables):
  - `export $(cat ~/.config/crontab-custom-ia/env | xargs)`
3. Run the wrapper to test the planner now:
  - `bash /home/user/data/crontab-custom-ia/jobs/run_weekly_planner.sh`
4. If you need to run the planner directly for debugging:
  - `python3 /home/user/data/crontab-custom-ia/weekly_content_planner.py`
5. Verify crontab installation and schedule:
  - `crontab -l` (look for the `# crontab-custom-ia` block). If missing, run `bash tools/crontab-custom-ia/install_crontab.sh`.
6. To publish the RFC/article:
  - Edit `content/posts/2025-12-30-assistant-context-standard/index.md` and set `draft: false`, then `git add`/`commit`/`push`.
  - Optionally, open the RFC issue: `bash tools/rfcs/open_rfc_issue.sh` (requires local `GITHUB_TOKEN`).

Commands to inspect repository and state:
- `git status --porcelain`
- `git log --oneline -n 10`
- `ls -la tools/crontab-custom-ia/`
- `ls -la /home/user/data/crontab-custom-ia/`

Security notes:
- Never commit `~/.config/crontab-custom-ia/env` or any secrets; `tools/crontab-custom-ia/env.example` exists as a safe template.
- For GitHub Actions use `secrets.GITHUB_TOKEN` or repository secrets, not plaintext files.

Resume metadata:
- prepared_for: future-assistant-or-engineer
- prepared_by: assistant
- prepared_on: 2025-12-31T12:00:00+01:00

Notes for the next assistant:
- Follow the `ASSISTANT_CONTEXT` RFC in `tools/rfcs/` when adding context to repo. Keep the snapshot brief and include next steps.
- If running automation that creates issues, prefer dry-run unless the owner confirms tokens are present and intended.

```
