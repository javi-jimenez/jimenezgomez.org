#!/usr/bin/env python3
"""
Generate simple SVG OG and thumbnail images for posts missing images.

Creates `og-image.svg` (1200x630) and `thumb.svg` (400x400) inside each
post folder under `content/posts/` that doesn't already contain an image file.

Usage: python3 scripts/generate_missing_images.py
"""
import hashlib
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "content" / "posts"
IMG_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"}


def slug_to_color(s):
    h = hashlib.sha1(s.encode("utf-8")).hexdigest()
    # take first 6 hex as color
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return f"rgb({r},{g},{b})"


def slug_to_accent(s):
    h = hashlib.sha1(s.encode("utf-8")).hexdigest()
    # take next 6 hex as accent color
    r = int(h[6:8], 16)
    g = int(h[8:10], 16)
    b = int(h[10:12], 16)
    return f"rgb({r},{g},{b})"


def read_title_and_blurb(md_path: Path, blurb_len=120):
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r"^---\s*$(.*?)^---\s*$", text, re.S | re.M)
    title = None
    if m:
        fm = m.group(1)
        mt = re.search(r"^title:\s*(?:\"|\')?(.*?)(?:\"|\')?\s*$", fm, re.M)
        if mt:
            title = mt.group(1).strip()
    # fallback: first H1 or folder name
    if not title:
        m2 = re.search(r"^#\s+(.*)$", text, re.M)
        if m2:
            title = m2.group(1).strip()
        else:
            title = md_path.parent.name

    # derive a short blurb from the first paragraph/content
    body = text
    # remove frontmatter
    if m:
        body = text[m.end():]
    # find first paragraph
    p = re.search(r"\n\s*\n([\s\S]{10,800}?)\n\s*\n", "\n"+body+"\n", re.M)
    if p:
        blurb = p.group(1).strip().replace("\n", " ")
    else:
        # fallback to first 160 chars of body
        plain = re.sub(r"\s+", " ", body).strip()
        blurb = plain[:blurb_len]

    # trim blurb
    if len(blurb) > blurb_len:
        blurb = blurb[:blurb_len].rsplit(' ',1)[0] + '...'

    return title, blurb


def has_image_files(folder: Path):
    for p in folder.iterdir():
        if p.suffix.lower() in IMG_EXTS and p.name.lower() not in {"og-image.svg", "thumb.svg"}:
            return True
    return False


OG_SVG = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"630\" viewBox=\"0 0 1200 630\"> 
    <defs>
        <linearGradient id=\"g1\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"> 
            <stop offset=\"0%\" stop-color=\"{bg}\" stop-opacity=\"1\"/>
            <stop offset=\"100%\" stop-color=\"{accent}\" stop-opacity=\"1\"/>
        </linearGradient>
    </defs>
    <rect width=\"100%\" height=\"100%\" fill=\"url(#g1)\" />
    <g opacity=\"0.07\"> 
        <circle cx=\"200\" cy=\"120\" r=\"160\" fill=\"white\" />
        <circle cx=\"980\" cy=\"460\" r=\"220\" fill=\"white\" />
    </g>
    <g transform=\"translate(80,120)\"> 
        <rect x=\"0\" y=\"0\" width=\"1040\" height=\"390\" rx=\"20\" fill=\"rgba(255,255,255,0.05)\" />
        <text x=\"520\" y=\"110\" font-family=\"Georgia, 'Times New Roman', serif\" font-weight=\"700\" font-size=\"44\" fill=\"#ffffff\" text-anchor=\"middle\">{title}</text>
        <foreignObject x=\"80\" y=\"150\" width=\"880\" height=\"200\">
            <body xmlns=\"http://www.w3.org/1999/xhtml\" style=\"color:#e6eef8;font-family:Inter, Arial, sans-serif;font-size:20px;line-height:1.3;\">{subtitle}</body>
        </foreignObject>
    </g>
    <g>
        <text x=\"1100\" y=\"610\" font-family=\"Inter, Arial, sans-serif\" font-size=\"14\" fill=\"rgba(255,255,255,0.6)\" text-anchor=\"end\">jimenezgomez.org</text>
    </g>
</svg>
"""

THUMB_SVG = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"400\" height=\"400\" viewBox=\"0 0 400 400\"> 
    <defs>
        <linearGradient id=\"tg\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"> 
            <stop offset=\"0%\" stop-color=\"{bg}\"/>
            <stop offset=\"100%\" stop-color=\"{accent}\"/>
        </linearGradient>
    </defs>
    <rect width=\"100%\" height=\"100%\" fill=\"url(#tg)\" rx=\"18\"/>
    <g>
        <circle cx=\"320\" cy=\"80\" r=\"60\" fill=\"rgba(255,255,255,0.06)\" />
        <rect x=\"24\" y=\"220\" width=\"352\" height=\"120\" rx=\"12\" fill=\"rgba(255,255,255,0.06)\" />
        <text x=\"200\" y=\"280\" font-family=\"Georgia, serif\" font-size=\"72\" fill=\"#ffffff\" text-anchor=\"middle\">{initials}</text>
    </g>
</svg>
"""


def initials_from_title(title: str):
    parts = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", title)
    if not parts:
        return title[:2].upper()
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()


def choose_symbol(title: str, blurb: str):
    """Choose a symbolic drawing type based on title/blurb keywords."""
    s = (title + " " + blurb).lower()
    if any(k in s for k in ("callback", "async", "promise", "js", "javascript", "node", "code")):
        return "code"
    if any(k in s for k in ("context", "assistant", "assistant_context", "session", "ai", "llm")):
        return "chat"
    if any(k in s for k in ("architecture", "layer", "network", "nodes", "microservice", "ddnsc")):
        return "network"
    if any(k in s for k in ("design", "brand", "logo", "visual", "identity")):
        return "star"
    if any(k in s for k in ("security", "auth", "token", "lock", "ssl")):
        return "lock"
    if any(k in s for k in ("book", "read", "guide", "tutorial")):
        return "book"
    if any(k in s for k in ("tool", "automation", "ci", "cli", "script")):
        return "gear"
    return "abstract"


def symbol_svg(kind: str, size: int = 160, fill: str = "rgba(255,255,255,0.12)"):
    """Return an SVG fragment (group) for a simple symbol."""
    if kind == "code":
        return f"<g fill=\"{fill}\"><rect x=\"0\" y=\"0\" width=\"{size}\" height=\"{size}\" rx=\"12\"/><text x=\"{size/2}\" y=\"{size/2+10}\" font-family=\"monospace\" font-size=\"{int(size/5)}\" fill=\"white\" text-anchor=\"middle\">&lt;/&gt;</text></g>"
    if kind == "chat":
        tail = int(size*0.18)
        return f"<g fill=\"{fill}\"><rect x=\"0\" y=\"0\" width=\"{size}\" height=\"{int(size*0.72)}\" rx=\"{int(size*0.08)}\"/><polygon points=\"{int(size*0.5)},{int(size*0.72)} {int(size*0.5)+tail},{int(size*0.72)} {int(size*0.5)},{int(size*0.72)+tail}\" fill=\"{fill}\"/></g>"
    if kind == "network":
        # three nodes connected
        a = int(size*0.2); b = int(size*0.5); c = int(size*0.8); y1 = int(size*0.35); y2 = int(size*0.65)
        return f"<g fill=\"{fill}\"><circle cx=\"{a}\" cy=\"{y1}\" r=\"{int(size*0.08)}\"/><circle cx=\"{b}\" cy=\"{y2}\" r=\"{int(size*0.08)}\"/><circle cx=\"{c}\" cy=\"{y1}\" r=\"{int(size*0.08)}\"/><line x1=\"{a}\" y1=\"{y1}\" x2=\"{b}\" y2=\"{y2}\" stroke=\"{fill}\" stroke-width=\"{int(size*0.04)}\" stroke-linecap=\"round\"/><line x1=\"{b}\" y1=\"{y2}\" x2=\"{c}\" y2=\"{y1}\" stroke=\"{fill}\" stroke-width=\"{int(size*0.04)}\" stroke-linecap=\"round\"/></g>"
    if kind == "star":
        return f"<g fill=\"{fill}\"><polygon points=\"{size*0.5},{size*0.1} {size*0.6},{size*0.4} {size*0.95},{size*0.4} {size*0.67},{size*0.6} {size*0.8},{size*0.95} {size*0.5},{size*0.74} {size*0.2},{size*0.95} {size*0.33},{size*0.6} {size*0.05},{size*0.4} {size*0.4},{size*0.4}\"/></g>"
    if kind == "lock":
        return f"<g fill=\"{fill}\"><rect x=\"{int(size*0.18)}\" y=\"{int(size*0.42)}\" width=\"{int(size*0.64)}\" height=\"{int(size*0.42)}\" rx=\"{int(size*0.06)}\"/><path d=\"M{int(size*0.5)} {int(size*0.42)} v-{int(size*0.18)} a{int(size*0.18)} {int(size*0.18)} 0 0 1 {int(size*0.36)} 0 v{int(size*0.18)}\" fill=\"{fill}\"/></g>"
    if kind == "book":
        return f"<g fill=\"{fill}\"><rect x=\"{int(size*0.12)}\" y=\"{int(size*0.12)}\" width=\"{int(size*0.76)}\" height=\"{int(size*0.64)}\" rx=\"6\"/><line x1=\"{int(size*0.28)}\" y1=\"{int(size*0.28)}\" x2=\"{int(size*0.72)}\" y2=\"{int(size*0.28)}\" stroke=\"white\" stroke-width=\"2\"/></g>"
    if kind == "gear":
        # simple gear-like circle with teeth
        return f"<g fill=\"{fill}\"><circle cx=\"{int(size*0.5)}\" cy=\"{int(size*0.5)}\" r=\"{int(size*0.22)}\"/><circle cx=\"{int(size*0.5)}\" cy=\"{int(size*0.5)}\" r=\"{int(size*0.08)}\" fill=\"rgba(255,255,255,0.2)\"/></g>"
    # abstract
    return f"<g fill=\"{fill}\"><rect x=\"0\" y=\"0\" width=\"{size}\" height=\"{int(size*0.6)}\" rx=\"{int(size*0.06)}\"/></g>"


def generate_for_post(folder: Path):
    md = folder / "index.md"
    if not md.exists():
        return False
    if has_image_files(folder):
        return False
    title, blurb = read_title_and_blurb(md, blurb_len=120)
    bg = slug_to_color(folder.name)
    initials = initials_from_title(title)

    og_path = folder / "og-image.svg"
    thumb_path = folder / "thumb.svg"

    # Compose OG with title and blurb
    og_text = escape_xml(title)
    og_sub = escape_xml(blurb)
    accent = slug_to_accent(folder.name)
    og_content = OG_SVG.format(bg=bg, accent=accent, title=og_text, subtitle=og_sub)

    thumb_content = THUMB_SVG.format(bg=bg, accent=accent, initials=escape_xml(initials))

    og_path.write_text(og_content, encoding="utf-8")
    thumb_path.write_text(thumb_content, encoding="utf-8")
    return True


def escape_xml(s: str):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))


def main():
    created = 0
    for child in sorted(POSTS.iterdir()):
        if not child.is_dir():
            continue
        if generate_for_post(child):
            print(f"Created images for {child.name}")
            created += 1
    print(f"Done. Created images for {created} posts.")


if __name__ == "__main__":
    main()
