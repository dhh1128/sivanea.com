# scripts/

Durable quality tooling for sivanea.com. (Not to be confused with `tools/`,
which holds the one-shot WordPress → Jekyll migration scripts and is historical.)

## `check_site.py`

The offline, Jekyll-aware quality gate. Run it from the repo root:

```bash
python3 scripts/check_site.py        # needs pyyaml
```

It proves the structural cleanliness of the content and exits non-zero if any
check fails:

1. **Frontmatter** parses as YAML and every page has a non-empty `title`
   (`README.md` is exempt — it is the GitHub landing page, not a Jekyll page).
2. **Internal page links** resolve to a real `.md` file (Jekyll slug rules:
   `href="some-poem"` → `some-poem.md`, relative to the linking page).
3. **Local asset references** (`assets/…`, images, audio, video, PDFs) exist
   on disk.
4. **No WordPress residue** (`[caption]`, `wp-content`) has crept back in.

External link and external-image liveness are intentionally **out of scope** —
that is covered by Lychee in `.github/workflows/link-check.yml`. Credited
external images (e.g. Flickr photos) are an accepted choice here, so they are
reported for awareness but never fail the check.

CI runs this on every push/PR via `.github/workflows/check.yml`.
