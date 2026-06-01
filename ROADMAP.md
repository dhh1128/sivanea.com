# Roadmap

Cleanup plan for the sivanea.com creative-writing site (poetry, lyrics, short
stories, plays, novels, essays, photography, art, music) after its migration
from WordPress to Jekyll.

_Created 2026-06-01._

## Scope decision

A sister repo, `../codecraft.co`, went through a much larger arc (a 124-essay
software anthology being groomed into an Amazon KDP **book**: permanent item-IDs,
a controlled tag vocabulary, a full metadata schema, image-ownership to zero
external dependencies, a Jekyll → Zensical platform migration, per-essay PDFs,
and a 12-file pytest suite). **Almost none of that machinery ports here**,
because sivanea has no book, no per-item PDF, and no professional-anthology SEO
goal — and because this repo migrated far more cleanly to begin with (no broken
YAML fences, no `[caption]`/`wp-content` residue, no mojibake in content,
`redirect_from` already preserved on 52 pages, section index pages already
curated and correctly linked, ~108/128 images already local).

So the goal here is narrow: **fix the genuine breakage, and stand up a
lightweight, proportionate proof that the content is and stays clean.**

## Done

- [x] **Layout HTML bugs** in `_layouts/default.html`: the migration-mangled IE
      conditional comment (`<! &mdash; [if lt IE 9]>` → `<!--[if lt IE 9]>`) and
      the mismatched `<h3>Comments</h2>` → `</h3>` (affected all 13 commented
      pages).
- [x] **Title-less pages**: `ai-art.md` and `ai-collab.md` had no frontmatter
      (rendering a blank `<h1>`); added `title`/`slug`.
- [x] **CI security + runtime**: bumped `lycheeverse/lychee-action`
      `v1.10.0` → `v2.8.0` (the `<2.0.2` arbitrary-code-injection fix Dependabot
      flagged on the sister repo) and `actions/checkout` `v4` → `v6` (node20 →
      node24) in `link-check.yml`.
- [x] **Proof harness**: `scripts/check_site.py` — offline, Jekyll-aware checker
      proving frontmatter validity + non-empty titles, internal page/asset link
      resolution, and no WordPress residue. Green today: 101 pages, 343 internal
      links, 0 problems. Wired into CI via `.github/workflows/check.yml`
      (`checkout@v6` + `setup-python@v6`, both node24).

## Standing policy (decided)

- **External images stay.** The ~20 remaining `staticflickr.com` images are
  either the author's own photostream or deliberately-credited third-party
  photos (the `viking/photo-gallery.md` casting mood-board, photographer credits
  in figcaptions). Unlike codecraft, the goal is **not** "own 100% of images" —
  it is "external images still resolve," which Lychee verifies in CI. The
  checker reports the external-image count for awareness but never fails on it.
- **Reader comments stay inline.** The 13 pages with migrated WordPress comments
  render them in an always-open section (now with valid HTML). No need for
  codecraft's collapsed-appendix treatment.
- **Mechanical edits only.** As in the sister repo: fix structure, links, images,
  and metadata; never rewrite the author's prose.

## Deliberately NOT doing (ported from codecraft, but not warranted here)

- Permanent item-IDs, controlled tag vocabulary, rich metadata schema
  (keywords/abstract/version/status), per-item PDFs, the book/KDP pipeline, and
  the Jekyll → Zensical platform migration. No goal here drives them.

## Optional / deferred (low value — debate before doing)

- [ ] Strip cosmetic WordPress-era markup (`zem_slink`, `wp-image-144` classes,
      inline `style=` attributes) — harmless, purely cosmetic.
- [ ] Add the orphan `blue.md` to the `poetry.md` index (or confirm it is
      intentionally unlisted).
- [ ] Decide how the `by:` field (on `broken-things.md`, `hidden-grace.md`,
      `showin-up.md`) should surface authorship in the layout.
- [ ] Archive the historical `tools/` migration scripts (they are inert).
- [ ] **Make the page layout explicit.** Production (GitHub Pages / Jekyll 3.10)
      auto-applies `layout: default` to every page, so `_layouts/default.html`
      (title, date, comments, CC footer) renders live — but no page declares a
      layout and `_config.yml` sets no `defaults`, so a local
      `bundle exec jekyll build` (Jekyll 4 + remote_theme) renders bare,
      layout-less pages. Adding `defaults: [{scope: {path: ""}, values:
      {layout: default}}]` to `_config.yml` is a no-op for production but makes
      local builds faithful and removes the reliance on implicit GitHub Pages
      behaviour. Outward-facing config — confirm before applying.
