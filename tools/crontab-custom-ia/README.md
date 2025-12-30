# crontab-custom-ia

This folder contains a simple meta-runner and job scaffolding to run local IA-related scripts via the user's `crontab`.

Structure:
- `run_cron_meta.sh` - executes every executable script in `jobs/` and logs to `logs/cron.log`.
- `jobs/` - place executable job scripts here (e.g., `run_weekly_planner.sh`).
- `weekly_content_planner.py` - local copy of the planner (can be executed from `jobs/` via a wrapper).
- `run_weekly_planner.sh` - wrapper to run `weekly_content_planner.py` with sane defaults.
- `install_crontab.sh` - adds a marked crontab entry for the current user.

Quick install (local):

1. Make scripts executable:

```bash
chmod +x ~/data/crontab-custom-ia/*.sh
chmod +x ~/data/crontab-custom-ia/jobs/* || true
```

2. Move wrappers to `jobs/` so the meta-runner executes them:

```bash
mkdir -p ~/data/crontab-custom-ia/jobs
mv ~/data/crontab-custom-ia/run_weekly_planner.sh ~/data/crontab-custom-ia/jobs/
```

3. Optional: set `GITHUB_REPOSITORY` and `GITHUB_TOKEN` in your environment if you want the planner to open issues on GitHub.

4. Install crontab entry (defaults to Mondays 09:00):

```bash
~/data/crontab-custom-ia/install_crontab.sh
```

Customize schedule via `CRON_SCHEDULE_OVERRIDE` env var before running installer, e.g.: 

```bash
export CRON_SCHEDULE_OVERRIDE="0 7 * * 1" # Mondays 07:00
~/data/crontab-custom-ia/install_crontab.sh
```

Notes:
- Scripts and logs live in `~/data/crontab-custom-ia/` for easy backup.
- `run_cron_meta.sh` will run any executable file in `jobs/` — ensure wrappers are safe and idempotent.
