# AI Coding Agent Instructions for jimenezgomez.org

## Project Overview

This is a **Hugo static site** using the Stack theme for a personal blog about software architecture, open source projects, and technology. The site is deployed via FTP to OVH hosting on every push.

## Architecture & Structure

- **Hugo Theme**: Uses `themes/stack` (Card-style blog theme)
- **Content**: Blog posts in `content/posts/YYYY-MM-DD-slug/index.md` with co-located images
- **Dual Landing**: Root `index.html` is a standalone portfolio page (Spanish), while Hugo generates blog under `/posts`
- **No Build Process**: Project deploys raw files via FTP - Hugo builds happen server-side or aren't shown in workflow

### Key Directories

- `content/posts/`: Each post is a folder with `index.md` + images
- `public/`: Hugo-generated static output (Git-tracked for deployment)
- `themes/stack/`: Third-party theme (do not modify directly)
- `layouts/_default/`: Empty - relies on theme layouts

## Content Conventions

### Blog Post Structure
Posts follow this pattern in `content/posts/YYYY-MM-DD-title/`:

```markdown
---
title: "Post Title"
date: 2025-04-04T11:09:00+02:00
draft: false
layout: post
image: "optional-featured-image.png"  # Co-located in same folder
---

Content here with markdown and HTML mixed.
Images use relative paths: ![Alt](image.png)
```

**Critical patterns:**
- Date format in folder: `YYYY-MM-DD-slug`
- All posts use `layout: post` (not Hugo default)
- Images stored alongside `index.md`, not in `/static`
- Mix of Spanish and English content (Spanish dominant)
- Posts can embed HTML/CSS inline (see 2025-12-02 SPA post)

### Archetype Template
`archetypes/default.md` uses TOML front matter (+++), but actual posts use YAML (---). New posts should follow existing YAML pattern.

## Development Workflow

### Creating New Posts
```bash
# Manual approach (recommended - follows existing pattern)
mkdir content/posts/YYYY-MM-DD-slug
touch content/posts/YYYY-MM-DD-slug/index.md
# Add YAML frontmatter with layout: post
```

### Hugo Configuration
`hugo.toml` sets:
- `mainSections = ['posts']` - only posts section displayed
- `unsafe = true` in goldmark - allows raw HTML in markdown
- Theme: `stack`

### Deployment
GitHub Actions (`.github/workflows/deploy-jimenezgomez.org.yml`):
- Triggers on every push
- FTP deploys entire repo to OVH at `/jimenezgomez.org/`
- No build step - likely server-side Hugo build or pre-built public/ folder

**Important**: Any file changes deploy immediately. Test locally before pushing.

## Project-Specific Patterns

1. **Dual Site Architecture**: Root `index.html` is separate portfolio (GitHub dark theme style), Hugo blog lives under `/posts`
2. **No npm/build tools**: Pure Hugo + manual theme
3. **Image handling**: Always co-locate with posts, never use `/static` for post images
4. **Content philosophy**: Posts focus on software architecture concepts (VBD/VERO architecture, layers, microservices)
5. **AI experimentation**: Recent posts explore AI-assisted development (see 2025-02-25, 2025-12-02)

## Common Tasks

**Add new blog post:**
1. Create `content/posts/YYYY-MM-DD-title/` folder
2. Add `index.md` with YAML frontmatter including `layout: post`
3. Place images in same folder
4. Commit and push (auto-deploys)

**Update portfolio page:**
- Edit root `index.html` directly (standalone file, not Hugo-generated)

**Modify Hugo config:**
- Edit `hugo.toml` for site-wide settings
- Theme customization requires overriding in `layouts/` (currently unused)

## Dependencies

- Hugo (extended version required by Stack theme)
- Stack theme from `themes/stack/`
- No JavaScript build process
- No package managers (npm/yarn)

## Testing Locally

```bash
hugo server -D  # Serve with drafts
hugo server     # Production preview
```

Access at `http://localhost:1313`
