#!/usr/bin/env bash
# Wrapper to run the weekly content planner with sane env defaults

BASE_DIR="/home/user/data/crontab-custom-ia"
SCRIPT="$BASE_DIR/weekly_content_planner.py"
LOG_DIR="$BASE_DIR/logs"
mkdir -p "$LOG_DIR"

export GITHUB_REPOSITORY=""
export GITHUB_TOKEN=""
# You can override SCHEDULE_DAYS, TOP_N, PLANNER_AUTHOR, PLANNER_LOCATION via env or export in crontab
export SCHEDULE_DAYS="7"
export TOP_N="5"
export PLANNER_AUTHOR="Francisco Javier"
export PLANNER_LOCATION="Valencia, España"

if [ ! -f "$SCRIPT" ]; then
  echo "Planner script not found at $SCRIPT" >&2
  exit 1
fi

python3 "$SCRIPT"
