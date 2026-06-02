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
- [x] **Made `link-check` meaningful.** It had been red on every push for
      months. Fixed the one real dead link (Cordimancy's `j.mp/1Mfr42y` Kindle
      404 → the live Amazon product page) and taught `.github/lychee.toml` to
      skip hosts that bot-block automated checkers (distrokid, 99designs — same
      pattern as the existing openart/midjourney/openai excludes) and to
      tolerate transient `429` rate-limiting (e.g. upload.wikimedia.org). Now
      green when links are genuinely fine, red only for real breakage.
- [x] **Homepage full-text search.** Live search box on `index.md` powered by
      vendored Lunr.js (`assets/js/lunr.min.js`) + a Liquid-generated
      `search.json` index (built by the legacy Pages pipeline, no plugin) +
      `assets/js/search.js`. Stemmed-term **and** trailing-wildcard query per
      word (whole-word + prefix matching), title-boosted ranking, highlighted
      snippets; degrades to the plain Contents list with no JS. `check_site.py`
      guards the wiring; coverage is by construction (index = published pages).
- [x] **Proof harness**: `scripts/check_site.py` — offline, Jekyll-aware checker
      proving frontmatter validity + non-empty titles, internal page/asset link
      resolution, no WordPress residue (incl. `zem_slink`/`wp-image`), no stray
      CI badge on a published page, **no orphan pages**, and the search wiring.
      Green today: 103 pages, 349 internal links, 0 problems. Wired into CI via
      `.github/workflows/check.yml` (`checkout@v6` + `setup-python@v6`, node24).

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

## Optional / deferred

All previously-listed optional items are now done:

- [x] Stripped WordPress-era markup (`zem_slink`/`wp-image` classes, lone Zemanta
      `rel`s) and moved inline `style=` to semantic CSS classes (`.note`,
      `.dedication`, `.text-right`, `.pubdate`); residue tripwire extended.
- [x] `blue.md` (a poem with a photo) now listed in both `poetry.md` and
      `photography.md`; an orphan-page check in `check_site.py` proves no page is
      unreachable (it also caught 3 mis-linked `viking/` companion pages).
- [x] The stray `by:` line on `broken-things`/`hidden-grace`/`showin-up` is now
      running-text authorship ("Lyrics are by …"), matching the other songs — no
      layout byline.
- [x] Deleted the inert `tools/` WordPress-migration scripts (git history is the
      archive).

_(none outstanding)_
