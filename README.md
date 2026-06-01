# Sivanea

[![check site structure](https://github.com/dhh1128/sivanea.com/actions/workflows/check.yml/badge.svg)](https://github.com/dhh1128/sivanea.com/actions/workflows/check.yml)
[![check links](https://github.com/dhh1128/sivanea.com/actions/workflows/link-check.yml/badge.svg)](https://github.com/dhh1128/sivanea.com/actions/workflows/link-check.yml)

*creative projects by Daniel Hardman*

A curated collection of poetry, lyrics, short stories, plays, novels, essays,
photography, and art — published at **[sivanea.com](https://sivanea.com)**.

This repository holds the content (Markdown), the owned media (`assets/`), and a
small Python checker that proves the content stays structurally clean. The site
is a plain Jekyll site published with GitHub Pages.

> The cleanup plan and scope live in **[ROADMAP.md](ROADMAP.md)**.

## Quick start

```bash
git clone git@github.com:dhh1128/sivanea.com.git
cd sivanea.com
bundle install
bundle exec jekyll serve     # local preview at http://127.0.0.1:4000
```

Run the structural checker — the offline half of the quality gate (Lychee
covers external links in CI):

```bash
pip install pyyaml
python3 scripts/check_site.py
```

## How it's organized

The root-level `*.md` files are the content — one file per piece, filename ==
slug. `index.md` is the site's table of contents (the homepage); the section
pages (`poetry.md`, `short-stories.md`, …) list the pieces in each genre. Media
lives in `assets/`. **This README is not part of the published site.**

| Path | What |
|---|---|
| `*.md` | content pieces (one per file) |
| `index.md` | site homepage / table of contents |
| `assets/` | images, audio, video, PDFs |
| `scripts/check_site.py` | offline clean-proof (frontmatter, links, assets, WP residue) |
| `_layouts/` `_includes/` `_config.yml` | Jekyll site setup |
| `.github/workflows/` | CI: structural check + external link check |
| `ROADMAP.md` | cleanup plan and scope |

## License

Content is licensed
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) unless
otherwise noted.
