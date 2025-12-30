#!/usr/bin/env python3
"""
Weekly content planner

Fetches a few public RSS feeds (Hacker News frontpage, arXiv cs.AI), extracts top items,
checks last published post date in `content/posts` (non-draft) and creates a GitHub issue
with a reminder and topic suggestions.

Environment variables:
- GITHUB_REPOSITORY
- GITHUB_TOKEN
- SCHEDULE_DAYS (default 7)
- TOP_N (topics per feed, default 5)
"""
import os
import sys
import json
import re
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET

REPO = os.environ.get('GITHUB_REPOSITORY')
TOKEN = os.environ.get('GITHUB_TOKEN')
SCHEDULE_DAYS = int(os.environ.get('SCHEDULE_DAYS', '7'))
TOP_N = int(os.environ.get('TOP_N', '5'))
# Planner author info (can be overridden via environment)
AUTHOR_NAME = os.environ.get('PLANNER_AUTHOR', 'Francisco Javier')
AUTHOR_LOCATION = os.environ.get('PLANNER_LOCATION', 'Valencia, España')

POSTS_DIR = Path('content/posts')

FEEDS = [
    ('HackerNews', 'https://hnrss.org/frontpage'),
    ('arXiv cs.AI', 'https://export.arxiv.org/rss/cs.AI'),
]


def fetch_feed(url):
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return resp.read()
    except Exception as e:
        print(f'Failed to fetch {url}: {e}', file=sys.stderr)
        return None


def parse_rss_items(xml_bytes, top_n=5):
    items = []
    try:
        root = ET.fromstring(xml_bytes)
    except Exception as e:
        return items
    # support rss and atom
    for item in root.findall('.//item')[:top_n]:
        title = item.findtext('title') or ''
        link = item.findtext('link') or ''
        items.append({'title': title.strip(), 'link': link.strip()})
    # atom fallback
    if not items:
        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry')[:top_n]:
            title = entry.findtext('{http://www.w3.org/2005/Atom}title') or ''
            link_el = entry.find('{http://www.w3.org/2005/Atom}link')
            link = link_el.get('href') if link_el is not None else ''
            items.append({'title': title.strip(), 'link': link.strip()})
    return items


def latest_published_date():
    latest = None
    if not POSTS_DIR.exists():
        return None
    for md in POSTS_DIR.rglob('index.md'):
        try:
            text = md.read_text(encoding='utf-8')
        except Exception:
            continue
        if not text.startswith('---'):
            continue
        parts = text.split('---', 2)
        if len(parts) < 3:
            continue
        fm = parts[1]
        draft = False
        date_s = None
        for line in fm.splitlines():
            if ':' not in line:
                continue
            k, v = line.split(':', 1)
            k = k.strip().lower()
            v = v.strip().strip('"').strip("'")
            if k == 'draft':
                draft = v.lower() in ('true', 'yes', '1')
            if k == 'date':
                date_s = v
        if draft:
            continue
        if date_s:
            try:
                ds = date_s.replace(' ', 'T', 1)
                dt = datetime.fromisoformat(ds)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
            except Exception:
                try:
                    dt = datetime.strptime(date_s.split('T')[0], '%Y-%m-%d').replace(tzinfo=timezone.utc)
                except Exception:
                    continue
            if latest is None or dt > latest:
                latest = dt
    return latest


def create_issue(title, body):
    if not REPO or not TOKEN:
        print('Missing GITHUB_REPOSITORY or GITHUB_TOKEN; cannot create issue')
        return
    data = json.dumps({'title': title, 'body': body}).encode('utf-8')
    req = urllib.request.Request(f'https://api.github.com/repos/{REPO}/issues', data=data,
                                 headers={
                                     'Authorization': f'token {TOKEN}',
                                     'Accept': 'application/vnd.github.v3+json',
                                     'User-Agent': 'weekly-content-planner'
                                 })
    try:
        with urllib.request.urlopen(req) as resp:
            print('Issue created:', resp.status)
    except Exception as e:
        print('Failed to create issue:', e)


def main():
    topics = []
    for name, url in FEEDS:
        xml = fetch_feed(url)
        if not xml:
            continue
        items = parse_rss_items(xml, TOP_N)
        topics.append((name, items))

    latest = latest_published_date()
    now = datetime.now(timezone.utc)
    overdue = False
    message_lines = []
    message_lines.append('Recordatorio semanal de contenido')
    message_lines.append(f'Solicitado por: {AUTHOR_NAME} ({AUTHOR_LOCATION}) — {now.date().isoformat()}')
    message_lines.append('')
    if latest:
        delta = now - latest
        message_lines.append(f'Último post publicado: {latest.date().isoformat()} (hace {delta.days} días)')
        if delta.days >= SCHEDULE_DAYS:
            overdue = True
            message_lines.append(f'⚠️ Has superado la cadencia de publicación de {SCHEDULE_DAYS} días.')
    else:
        overdue = True
        message_lines.append('No se ha detectado ningún post publicado aún.')

    message_lines.append('')
    message_lines.append('Sugerencias de temas (extraídas automáticamente):')
    for name, items in topics:
        message_lines.append(f'\n**{name}**:')
        if not items:
            message_lines.append('- (no disponible)')
            continue
        for it in items:
            title = it.get('title')
            link = it.get('link')
            message_lines.append(f'- {title} — {link}')

    message_lines.append('')
    message_lines.append('Acciones sugeridas:')
    message_lines.append('- Escoge 1–3 temas de la lista para convertir en un post.\n- Responde a este issue con la selección o crea un draft en `content/posts`.')

    title = 'Agenda semanal de publicación — ' + (now.date().isoformat())
    body = '\n'.join(message_lines)
    if overdue:
        title = '[URGENTE] ' + title

    create_issue(title, body)


if __name__ == '__main__':
    main()
