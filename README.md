# Blazium Articles

This repository serves as a centralized space for all articles written by the team to publish on
the various platform we are active on (X, IndieDB, itch.io, Patreon), and on the Blazium CDN for
Blazium Hub News.

## Structure

Engine articles must use this layout (slug = folder name = file name, no spaces):

```
engine/
  <slug>/
    <slug>.md
    assets/          (optional)
      cover.jpg
      image1.png
```

Example: `engine/steam-module/steam-module.md`

## Frontmatter

```yaml
---
title: "Article Title"
description: "Short summary for listings and RSS."
cover: "assets/cover.jpg"
slug: "steam-module"
deployed: true
# optional:
# date: "2025-01-15"
# changes: https://github.com/...
hosts:
  - name: IndieDB
    url: https://www.indiedb.com/engines/blazium-engine/news/steam-module
  # - name: itch.io
  #   url: https://...
---
```

| Field | Required | Notes |
|-------|----------|-------|
| `title` | yes | Display title |
| `description` | yes | Summary / RSS description |
| `cover` | yes | Relative path to cover image |
| `slug` | **yes** | kebab-case `[a-z0-9-]+` only — **no spaces**. Must match path `engine/<slug>/<slug>.md` |
| `deployed` | yes for CDN | `true` publishes to CDN; `false` / missing skips publish |
| `date` | no | `YYYY-MM-DD`; defaults to git last-commit date at publish |
| `changes` | no | Changelog / milestone URL |
| `hosts` | no | Array of `{ name, url }` external places the article is hosted (IndieDB, itch.io, …). Shown in Hub News. May be empty, added before first CDN publish, or updated later and republished via sync. |

Only articles with `deployed: true` are validated for media completeness and uploaded to
`https://cdn.blazium.app/articles/`. `hosts` is optional for every article and is written into
CDN `meta.json` / `index.json` when present.

## Scripts

Under `/scripts`:

| Script | Purpose |
|--------|---------|
| `validate_articles.js` | Check frontmatter (incl. required slug/path) and deployed media |
| `publish_articles.js` | Build `dist/articles/` (RSS, index.json, per-slug meta/content/assets) |
| `md_to_html.js` | Convert markdown to IndieDB-friendly HTML (manual publish helper) |

```bash
cd scripts
npm ci
node validate_articles.js
node publish_articles.js
node md_to_html.js "engine/release-0-6-725/release-0-6-725.md"
```

For IndieDB/itch.io, **images/videos still need to be added manually** after `md_to_html.js`.

## CI / CDN

CDN target: DigitalOcean Spaces behind `https://cdn.blazium.app` (same bucket as CLI/Hub).

| Workflow | When | What |
|----------|------|------|
| **Publish Articles** | Push to `master`/`main` | Validate only |
| **Publish Articles** | PR opened / updated | Validate only |
| **Publish Articles** | PR merged into `master`/`main` | Validate → build → upload to CDN |
| **Sync Articles to CDN** | Manual (`workflow_dispatch`) | Full republish of all `deployed: true` articles |
| **Publish Articles** (manual) | Manual (`workflow_dispatch`) | Same full CDN republish (bootstrap / ops) |

Author flow: set `deployed: true` in a PR; merge to publish. Use **Actions → Sync Articles to CDN → Run workflow** for bootstrap or forced refresh.

### Repository secrets

| Secret | Purpose |
|--------|---------|
| `DO_ACCESS_KEY` | DigitalOcean Spaces access key |
| `DO_SECRET_KEY` | DigitalOcean Spaces secret |
| `DO_SPACE_NAME` | Spaces bucket name |
| `DO_SPACE_REGION` | e.g. `nyc3` |

### CDN layout

```
articles/rss.xml
articles/index.json
articles/{slug}/meta.json   # includes hosts: [{name,url}, ...]
articles/{slug}/content.bbcode
articles/{slug}/content.md
articles/{slug}/assets/...
```

Hub News lists articles from `rss.xml`, then loads `meta.json` (for `hosts`) and `content.bbcode` when an article is opened.
