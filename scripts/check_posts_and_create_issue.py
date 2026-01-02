#!/usr/bin/env python3
"""
Simple checker for Hugo posts drafts.
Finds posts under content/posts/*/index.md (or .md files) with `draft: true`
and with `date` in the past (i.e. scheduled date passed) or drafts older than a grace period.
If any pending items are found, creates a GitHub issue using `GITHUB_TOKEN`.

This script is intended to be run from a GitHub Action with `GITHUB_REPOSITORY` and
`GITHUB_TOKEN` set in the environment.
"""
import os
import sys
import re
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = os.environ.get('GITHUB_REPOSITORY')
TOKEN = os.environ.get('GITHUB_TOKEN')
DRIFT_DAYS = int(os.environ.get('REMINDER_DAYS', '30'))  # drafts older than this

POSTS_DIR = Path('content/posts')


def parse_frontmatter(path: Path):
    """Return dict with frontmatter keys 'draft' (bool) and 'date' (str) if present."""
    data = {}
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return data
    if not text.startswith('---'):
        return data
    parts = text.split('---', 2)
    if len(parts) < 3:
        return data
    fm = parts[1]
    for line in fm.splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        k, v = line.split(':', 1)
        k = k.strip()
        v = v.strip()
        if k.lower() == 'draft':
            data['draft'] = v.lower() in ('true', 'yes', '1')
        if k.lower() == 'date':
            data['date'] = v.strip().strip('"').strip("'")
    return data


def parse_date(s: str):
    # try iso formats, fallback to date-only
    if not s:
        return None
    s = s.strip()
    # Replace space between date and time with T if needed
    s2 = s.replace(' ', 'T', 1) if ' ' in s and 'T' not in s else s
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M%z", "%Y-%m-%d", "%Y-%m-%dT%H:%M"):
        try:
            dt = datetime.strptime(s2, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            continue
    # Last resort: try to parse prefix
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s2)
    if m:
        try:
            dt = datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None
    return None


def find_pending_posts():
    now = datetime.now(timezone.utc)
    pending = []
    if not POSTS_DIR.exists():
        return pending
    for post in POSTS_DIR.rglob('index.md'):
        fm = parse_frontmatter(post)
        draft = fm.get('draft', False)
        date_s = fm.get('date')
        date = parse_date(date_s) if date_s else None
        # file mtime as fallback
        mtime = datetime.fromtimestamp(post.stat().st_mtime, tz=timezone.utc)
        age_days = (now - mtime).days
        reason = None
        if draft:
            # If scheduled date in past, it's overdue
            if date and date < now:
                reason = f"scheduled date {date.isoformat()} has passed"
            elif age_days >= DRIFT_DAYS:
                reason = f"draft older than {DRIFT_DAYS} days (modified {mtime.date()})"
        if reason:
            rel = str(post.relative_to(Path.cwd()))
            pending.append({'path': rel, 'date': date_s or '', 'reason': reason})
    return pending


def create_issue(pending):
    if not REPO or not TOKEN:
        print('Missing GITHUB_REPOSITORY or GITHUB_TOKEN; skipping issue creation')
        return
    title = f"Recordatorio: {len(pending)} post(s) en borrador pendientes de publicación"
    body_lines = ["Se han detectado posts en `content/posts` que están en estado `draft` y requieren atención:\n"]
    for p in pending:
        body_lines.append(f"- {p['path']} — {p['reason']}\n")
    body_lines.append('\nSi quieres que publique o que revise, dime o actualiza el estado de los posts.')
    body = '\n'.join(body_lines)
    data = json.dumps({'title': title, 'body': body})
    import urllib.request
    req = urllib.request.Request(f'https://api.github.com/repos/{REPO}/issues', data=data.encode('utf-8'),
                                 headers={
                                     'Authorization': f'token {TOKEN}',
                                     'Accept': 'application/vnd.github.v3+json',
                                     'User-Agent': 'content-reminder-script'
                                 })
    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = resp.read().decode('utf-8')
            print('Issue created:', resp_data[:200])
    except Exception as e:
        print('Failed to create issue:', e)


def main():
    pending = find_pending_posts()
    if not pending:
        print('No pending drafts found')
        return
    print(f'Found {len(pending)} pending drafts')
    create_issue(pending)


if __name__ == '__main__':
    main()
