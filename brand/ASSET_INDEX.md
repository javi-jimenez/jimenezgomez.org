# Laia Brand Assets - Reference Index

This file keeps track of all visual identity resources of Laia and where they are mentioned/used.

## Resource Locations

### 1. Original Resources (Source)
**Location:** `content/posts/2025-12-18-laia-brand-identity/`

Created files:
- laia-brand-showcase.svg (post thumbnail)
- laia-brand-hero.svg (article hero)
- laia-logo-main.svg
- laia-logo-light.svg
- laia-logo-dark.svg
- laia-logo-mono.svg
- laia-icon-compact.svg
- laia-avatar-github.svg
- laia-avatar-twitter.svg
- laia-avatar-linkedin.svg
- laia-banner-github.svg
- laia-social-instagram.svg
- laia-social-twitter-card.svg

**Total:** 13 files SVG

### 2. Copied Resources (Distribution)
**Location:** `brand/`

Structure:
```
brand/
├── README.md                        # Documentation básica
├── brand-guidelines.pdf             # Manual completo (Markdown)
├── logo/
│   ├── laia-logo-main.svg
│   ├── laia-logo-light.svg
│   ├── laia-logo-dark.svg
│   └── laia-logo-mono.svg
├── icons/
│   └── laia-icon-compact.svg
├── avatars/
│   ├── laia-avatar-github.svg
│   ├── laia-avatar-twitter.svg
│   └── laia-avatar-linkedin.svg
├── banners/
│   └── laia-banner-github.svg
└── social/
    ├── laia-social-instagram.svg
    └── laia-social-twitter-card.svg
```

**Total:** 11 files SVG + 2 documents

## References in Blog Articles

### Article 1: Laia - Ethical Artificial Intelligence
**Location:** `content/posts/2025-12-18-laia-intelligent-agent/index.md`

**Used images:**
- `image: "laia-thumbnail.svg"` (frontmatter - thumbnail)
- `![Laia - Ethical AI Research](laia-header.svg)` (line 20 - header)

**Files in the folder:**
- laia-ai.jpg
- laia-ai.svg (not currently used)
- laia-header.svg
- laia-thumbnail.svg

### Article 2: Laia Visual Identity
**Location:** `content/posts/2025-12-18-laia-brand-identity/index.md`

**Images used in the article:**
1. Frontmatter: `image: "laia-brand-showcase.svg"`
2. Hero: `![Laia Brand Identity](laia-brand-hero.svg)`
3. Main Logo: `![Main Logo Laia](laia-logo-main.svg)`
4. Icono: `![Compact Icon](laia-icon-compact.svg)`
5. GitHub Avatar: `![GitHub Avatar](laia-avatar-github.svg)`
6. Twitter Avatar: `![Twitter Avatar](laia-avatar-twitter.svg)`
7. LinkedIn Avatar: `![LinkedIn Avatar](laia-avatar-linkedin.svg)`
8. Banner GitHub: `![GitHub Banner](laia-banner-github.svg)`
9. Logo Light: `![Logo Light](laia-logo-light.svg)`
10. Logo Dark: `![Logo Dark](laia-logo-dark.svg)`
11. Logo Mono: `![Logo Mono](laia-logo-mono.svg)`
12. Instagram: `![Instagram Template](laia-social-instagram.svg)`
13. Twitter Card: `![Twitter Card](laia-social-twitter-card.svg)`

**Resources section:** Documents the location in `content/posts/2025-12-18-laia-brand-identity/` and proposes future structure in `brand/`

## Documentation

### brand/README.md
- Folder structure description
- Reference to the blog and PDF
- CC BY 4.0 license information
- Contact

### brand/brand-guidelines.pdf (Markdown)
Secciones:
1. Introduction (project and purpose)
2. Design philosophy (stars, blue, neural network)
3. Color palette (primaries, neutrals, accent)
4. Logo (versions and uses)
5. Spacing and safe area
6. Typography (Segoe UI, Inter, Arial)
7. Allowed uses (backgrounds, applications)
8. Forbidden uses
9. Avatars for social networks
10. Banners y headers
11. Accessibility (WCAG AAA, color blindness)
12. Resource files (locations)
13. License (CC BY 4.0)
14. Version control
15. Credits

## Synchronization

### If an SVG is modified in the original post:
```bash
# Copy from post to brand/
cp content/posts/2025-12-18-laia-brand-identity/[archivo].svg brand/[subcarpeta]/
```

### If a new resource is created:
1. Create in `content/posts/2025-12-18-laia-brand-identity/`
2. Add it to the blog article with `![](nombre.svg)`
3. Copy it to `brand/[subcarpeta-apropiada]/`
4. Update this reference file
5. Update `brand/brand-guidelines.pdf` if applicable

## Color Palette (Quick Reference)

```css
/* Primaries */
--laia-blue-deep:    #0c4a6e  /* Deep blue */
--laia-blue-primary: #0369a1  /* Main blue */
--laia-blue-light:   #60a5fa  /* Light blue */
--laia-blue-pale:    #bfdbfe  /* Pale blue */

/* Neutrals */
--laia-dark:         #0f172a  /* Dark background */
--laia-slate:        #1e293b  /* Slate gray */
--laia-gray:         #94a3b8  /* Mid gray */
--laia-light:        #f0f9ff  /* Almost white */

/* Accent */
--laia-accent-cyan:  #06b6d4  /* Cyan */
--laia-accent-sky:   #38bdf8  /* Sky */
```

## Tipografía (Quick Reference)

- **Main:** Segoe UI (weight 300 titles, 400 text)
- **Web/Apps:** Inter
- **Fallback:** Arial
- **Letter-spacing:** 12-20px (logos), 3-8px (titles)

## Notes

- Los files SVG son la fuente principal (vectoriales, escalables)
- El post del blog es la ubicación canónica de los files originales
- The `brand/` folder is for distribution and external use
- Any change must be reflected in both locations
- The blog article serves as interactive visual documentation
- The PDF serves as formal documentation to print/share

## Last update
**Date:** 2025-12-18  
**Version:** 1.0  
**Changes:** Initial creation of the Laia visual identity system
