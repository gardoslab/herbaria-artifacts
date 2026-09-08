#!/usr/bin/env python3
"""Fails if any \\cite{...} key in writing/**/*.tex has no matching entry
in writing/benchmark-paper/refs.bib (the single Citation-agent-owned bib file). See T-1.9 -- this is the CI-time version of the
hallucinated-citation countermeasure Citation/Literature-Review (T-1.4)
already enforces at write time; this catches it even if refs.bib and the
manuscript drift apart across separate PRs.

Stdlib only -- runs in CI with no extra install step.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEX_GLOB = "writing/**/*.tex"
BIB_PATH = REPO_ROOT / "writing" / "benchmark-paper" / "refs.bib"

# \cite, \citep, \citet, \citeauthor, starred/optional-arg variants, and
# comma-separated multi-key citations (\cite{a,b,c}).
CITE_RE = re.compile(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]+)\}")
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")


def find_cite_keys(tex_text: str) -> set[str]:
    keys = set()
    for m in CITE_RE.finditer(tex_text):
        for key in m.group(1).split(","):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


def find_bib_keys(bib_text: str) -> set[str]:
    return {m.group(1).strip() for m in BIB_KEY_RE.finditer(bib_text)}


def main() -> int:
    tex_paths = sorted(REPO_ROOT.glob(TEX_GLOB))
    bib_text = BIB_PATH.read_text() if BIB_PATH.exists() else ""
    bib_keys = find_bib_keys(bib_text)

    all_cite_keys: set[str] = set()
    missing_by_file: dict[str, list[str]] = {}
    for tex_path in tex_paths:
        cite_keys = find_cite_keys(tex_path.read_text())
        all_cite_keys |= cite_keys
        missing = sorted(cite_keys - bib_keys)
        if missing:
            missing_by_file[str(tex_path.relative_to(REPO_ROOT))] = missing

    if missing_by_file:
        print("Undefined citation key(s) found:", file=sys.stderr)
        for tex_file, keys in missing_by_file.items():
            print(f"  {tex_file}: {', '.join(keys)}", file=sys.stderr)
        print(f"({len(bib_keys)} key(s) defined in {BIB_PATH.relative_to(REPO_ROOT)})", file=sys.stderr)
        return 1

    print(f"OK: all {len(all_cite_keys)} cite key(s) across {len(tex_paths)} file(s) resolve in refs.bib.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
