#!/usr/bin/env python3
"""Prove the sivanea.com content is structurally clean.

This is the offline, Jekyll-aware half of the site's quality gate. It proves
the things Lychee (the link-check workflow) does *not*:

  1. Frontmatter parses as YAML, and every page carries a non-empty `title`.
  2. Every internal page link resolves to a real `.md` file (Jekyll slug rules).
  3. Every local asset reference (`assets/...`, `*.pdf`, images, audio, video)
     exists on disk.
  4. No WordPress residue has crept back in (`[caption]`, `wp-content`).

External links and external image liveness are deliberately *out of scope* —
that is Lychee's job (see .github/workflows/link-check.yml). External images
(e.g. credited Flickr photos) are an accepted design choice here, not a defect,
so they are reported for awareness but never fail the check.

Exit status: 0 if clean, 1 if any problem is found. Run `python3 scripts/check_site.py`.
"""
from __future__ import annotations

import os
import re
import sys

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories that are build output, tooling, or VCS — never content pages.
SKIP_DIRS = {".git", "_site", ".jekyll-cache", "scripts", "tools", "assets"}

# Project docs (repo landing page, roadmap) are not Jekyll content pages: exempt
# from the title and WordPress-residue checks (they legitimately discuss terms
# like "[caption]" and "wp-content"). Their internal links are still validated.
PROJECT_DOCS = {"README.md", "ROADMAP.md"}

EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|data:|//|#)")
HAS_EXT = re.compile(r"\.[A-Za-z0-9]{1,6}$")

HTML_REF = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""")
MD_LINK = re.compile(r"\]\(\s*([^)\s]+)")  # [text](url ...) / ![alt](url ...)

RESIDUE = [re.compile(r"\[/?caption", re.I), re.compile(r"wp-content", re.I)]

# CI status badges belong in README (GitHub repo view), never on a published page.
BADGE = re.compile(r"badge\.svg|img\.shields\.io", re.I)


def pages() -> list[str]:
    found = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(".md"):
                found.append(os.path.join(root, f))
    return sorted(found)


def split_frontmatter(text: str):
    """Return (frontmatter_text_or_None, body). Frontmatter must open on line 1."""
    if not text.startswith("---\n") and text != "---":
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text  # opened a fence but never closed it
    fm = text[4:end]
    body = text[end + 4:]
    return fm, body


def link_targets(body: str):
    for m in HTML_REF.finditer(body):
        yield m.group(1)
    for m in MD_LINK.finditer(body):
        yield m.group(1)


def main() -> int:
    problems: list[str] = []
    external_imgs = 0
    n_links = 0
    files = pages()

    for path in files:
        rel = os.path.relpath(path, REPO)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()

        fm_text, body = split_frontmatter(text)

        # --- 1. frontmatter + title -------------------------------------
        fm = {}
        if fm_text is not None:
            try:
                fm = yaml.safe_load(fm_text) or {}
            except yaml.YAMLError as e:
                problems.append(f"{rel}: frontmatter is not valid YAML ({e.__class__.__name__})")
        is_doc = os.path.basename(rel) in PROJECT_DOCS
        if not is_doc:
            if fm_text is None:
                problems.append(f"{rel}: missing frontmatter (no title/date for the layout)")
            elif not str(fm.get("title", "")).strip():
                problems.append(f"{rel}: frontmatter has no non-empty `title`")

        # --- 4. WordPress residue + stray-badge tripwires ---------------
        if not is_doc:
            for pat in RESIDUE:
                if pat.search(body):
                    problems.append(f"{rel}: WordPress residue matched /{pat.pattern}/")
            if BADGE.search(body):
                problems.append(f"{rel}: CI status badge belongs in README, not a published page")

        # --- 2 + 3. internal links and local assets ---------------------
        for raw in link_targets(body):
            target = raw.split("#", 1)[0].strip()
            if not target or EXTERNAL.match(target):
                continue  # external / anchor — Lychee's job, not ours
            n_links += 1
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            last = os.path.basename(resolved)
            if HAS_EXT.search(last):
                ok = os.path.isfile(resolved)
                kind = "asset"
            else:
                ok = os.path.isfile(resolved + ".md")
                kind = "page"
            if not ok:
                problems.append(f"{rel}: broken internal {kind} link -> '{raw}'")

        # informational: external <img> count (not a failure)
        for m in re.finditer(r"<img[^>]+src=[\"'](https?://[^\"']+)", body):
            external_imgs += 1

    # ---------------------------------------------------------------------
    print(f"Scanned {len(files)} pages, {n_links} internal links.")
    print(f"External <img> references (Lychee's responsibility): {external_imgs}.")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nCLEAN: frontmatter valid, internal links + local assets resolve, no WP residue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
