# Quickstart: Bilingual README Implementation

**Feature**: 010-bilingual-readme
**Date**: 2026-01-20

## Overview

This guide explains how to implement the bilingual README.md for LegalDocs Manager.

## Prerequisites

- Access to repository root
- Knowledge of GitHub-Flavored Markdown
- Existing screenshots in `docs/screenshots/`

## Implementation Steps

### Step 1: Backup Current README

```bash
cp README.md README.md.backup
```

### Step 2: Create New README Structure

The new README follows this structure:

```
1. Header Block (centered, bilingual toggle, badges)
2. English Section (complete documentation)
3. Divider (horizontal rule with Spanish indicator)
4. Spanish Section (complete documentation)
```

### Step 3: Write Header Block

```markdown
<div align="center">

# LegalDocs Manager

🇺🇸 [English](#english) | 🇪🇸 [Español](#español)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.15-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Coverage](https://img.shields.io/badge/Coverage-98%25-brightgreen.svg)
![Tests](https://img.shields.io/badge/Tests-163%20passing-brightgreen.svg)

**A comprehensive legal document management system built with Django REST Framework**

**Sistema integral de gestión de documentos legales construido con Django REST Framework**

</div>
```

### Step 4: Write English Section

Start with the English anchor and TOC:

```markdown
---

<a name="english"></a>

## 🇺🇸 English

### Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
...
```

Then add all sections in order as defined in `contracts/readme-sections.md`.

### Step 5: Add Divider

```markdown
---

<div align="center">

# 🇪🇸 Español

[🇺🇸 Switch to English](#english)

</div>

<a name="español"></a>
```

### Step 6: Write Spanish Section

Mirror all English sections with Spanish translations:

```markdown
### Tabla de Contenidos

- [Características](#características)
- [Capturas de Pantalla](#capturas-de-pantalla)
...
```

### Step 7: Validate

1. **Check all links**: Every TOC link must navigate to correct section
2. **Verify images**: All screenshots must load correctly
3. **Test on GitHub**: Push and verify rendering on GitHub.com
4. **Mobile check**: Verify tables scroll horizontally on narrow screens

## Content Checklist

### Required Sections (Both Languages)

- [ ] Table of Contents
- [ ] Features list with icons
- [ ] Screenshots gallery (collapsible)
- [ ] Tech Stack
- [ ] Quick Start (5 steps)
- [ ] Installation (detailed)
- [ ] Environment Variables table
- [ ] Database Setup (PostgreSQL + SQLite)
- [ ] Running Tests
- [ ] Demo Data
- [ ] API Reference tables
- [ ] Project Structure tree
- [ ] Contributing guidelines
- [ ] License

### Screenshots to Include

From `docs/screenshots/`:

- [ ] 07-api/01-swagger-overview.png
- [ ] 01-auth/02-login-endpoint.png
- [ ] 02-clients/02-client-list-endpoint.png
- [ ] 03-cases/02-case-list-filters.png
- [ ] 03-cases/04-case-statistics-endpoint.png
- [ ] 04-documents/03-document-upload-endpoint.png
- [ ] 05-dashboard/01-dashboard-endpoint.png
- [ ] 06-admin/02-admin-dashboard.png
- [ ] 06-admin/04-admin-cases-list.png

## Verification

After implementation:

```bash
# Check file size (should be 600-800 lines)
wc -l README.md

# Verify no broken image links
grep -o '!\[.*\](.*\.png)' README.md | while read line; do
  path=$(echo "$line" | sed 's/.*](\(.*\))/\1/')
  if [ ! -f "$path" ]; then
    echo "Missing: $path"
  fi
done

# Push and verify on GitHub
git add README.md
git commit -m "docs: crear README bilingüe exhaustivo"
git push origin 010-bilingual-readme
```

## Troubleshooting

### Anchor Links Not Working

- Ensure anchor IDs are lowercase with hyphens
- GitHub auto-generates anchors from headers
- Test by clicking links after pushing to GitHub

### Tables Not Rendering

- Ensure header separator row exists: `|---|---|`
- Check for proper spacing around pipes

### Images Not Loading

- Use relative paths from repository root
- Verify file exists at specified path
- Check file extension case (`.png` vs `.PNG`)
