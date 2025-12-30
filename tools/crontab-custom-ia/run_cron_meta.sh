#!/usr/bin/env bash
# Meta-runner for custom IA cron jobs
# Executes every executable script in this folder's `jobs/` subfolder sequentially

set -euo pipefail

BASE_DIR="/home/user/data/crontab-custom-ia"
JOBS_DIR="$BASE_DIR/jobs"
LOG_DIR="$BASE_DIR/logs"
mkdir -p "$JOBS_DIR" "$LOG_DIR"

TIMESTAMP() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

echo "[$(TIMESTAMP)] Running cron meta-runner..." >> "$LOG_DIR/cron.log"

for job in "$JOBS_DIR"/*; do
  if [ -x "$job" ]; then
    echo "[$(TIMESTAMP)] Starting job: $job" >> "$LOG_DIR/cron.log"
    # Run job and capture stdout/stderr
    "$job" >> "$LOG_DIR/cron.log" 2>&1 || echo "[$(TIMESTAMP)] Job failed: $job" >> "$LOG_DIR/cron.log"
    echo "[$(TIMESTAMP)] Finished job: $job" >> "$LOG_DIR/cron.log"
  fi
done

echo "[$(TIMESTAMP)] All jobs finished." >> "$LOG_DIR/cron.log"
