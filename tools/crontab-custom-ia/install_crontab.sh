#!/usr/bin/env bash
# Install crontab entry for the user to run the meta-runner weekly

set -euo pipefail

BASE_DIR="/home/user/data/crontab-custom-ia"
METARUN="$BASE_DIR/run_cron_meta.sh"
LOG="${BASE_DIR}/logs/cron.log"
CRON_SCHEDULE="0 9 * * 1" # default: Mondays at 09:00

# Allow override via env var
if [ -n "${CRON_SCHEDULE_OVERRIDE:-}" ]; then
  CRON_SCHEDULE="$CRON_SCHEDULE_OVERRIDE"
fi

CRON_COMMENT="# crontab-custom-ia"
CRON_LINE="$CRON_SCHEDULE $METARUN >> $LOG 2>&1 $CRON_COMMENT"

existing=$(crontab -l 2>/dev/null || true)
if echo "$existing" | grep -q "$CRON_COMMENT"; then
  echo "Crontab entry already present. Skipping."
  exit 0
fi

echo "Installing crontab entry: $CRON_LINE"

(echo "$existing"; echo "$CRON_LINE") | crontab -
echo "Crontab installed."
