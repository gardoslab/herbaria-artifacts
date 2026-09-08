# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## What this repo is

LaTeX manuscripts for the herbaria research team, plus the CI that compiles them and lints
citations. **Slated to become `herbaria-artifacts`** (parent build-plan T-1.15): the current
tree moves under `writing/`, and a sibling `experiment-artifacts/{dir}/{cycle_id}/` subtree
becomes the git home for what experiment cycles produce (configs, job scripts, eval outputs,
agent-written scripts). Until that lands, the layout below is the live one.

It is a **submodule** of `gardoslab/herbaria-research-agent-design`, which holds
the governing documents (`herbaria-agent-framework-v2.md`, `herbaria-build-plan-v2.md`); the
agent code that writes into this repo lives in the sibling submodule
`gardoslab/herbaria-orchestrator`.

| Path | Contents |
|---|---|
| `benchmark-paper/main.tex` | The benchmark paper. Compiles locally with `pdflatex main.tex`. |
| `benchmark-paper/refs.bib` | The **only** citation source. Owned by the Citation/Literature-Review agent. |
| `benchmark-paper/figures/` | Promoted figures only, in per-direction subfolders. |
| `.github/workflows/latex.yml` | Builds `main.pdf` on every push/PR and fails on any `\cite` key missing from `refs.bib`. |

## Branching and PRs

**Never commit changes directly to `main` or to whatever branch current work is being
integrated into** — not for one-line fixes.

1. Before the first file modification, check the branch (`git status -sb`). This repo is
   usually checked out at a **detached HEAD** from the parent's submodule pin, so there is
   often no branch at all. Create a topic branch first:
   `git switch -c <type>/<short-description>`, where `<type>` is one of `feat`, `fix`,
   `refactor`, `docs`, `exp`, or `chore`. Say which branch you created rather than asking
   permission.
2. If you are already on a topic branch belonging to this task, stay on it. If it belongs to
   unrelated work, branch off `main` instead.
3. Commit related changes together; do not batch unrelated work into one commit.
4. Land the work with a pull request against `main` (`gh pr create`) and let it be reviewed
   and merged — never fast-forward or push the topic branch onto `main` yourself.
5. A merged PR here is **invisible to the parent repo** until someone bumps the submodule
   pointer there. That bump is a separate change on a parent topic branch, landing via its
   own PR, and it must point at the *merged* commit on `main`, not at your topic-branch
   commit. Do not bump the pointer before the PR here is merged.

If you find uncommitted changes already sitting on `main` or a detached HEAD, leave them
uncommitted.

## Rules specific to this repo

These are the human gates from the framework doc (§6.2, §7, §8.1); the agents enforce them
structurally and a human editing by hand should hold to the same lines.

- **`refs.bib` has one writer.** Only the Citation/Literature-Review agent writes it, on a
  `lit/refs-update` branch via PR. Do not add an entry by hand to make a `\cite` resolve;
  add it through that path so it is verified and deduplicated by DOI. Never invent a
  reference — flag it as unverifiable instead.
- **Every `\cite` must resolve in `refs.bib`.** CI (`check-citations`) fails the PR
  otherwise, and `build` is skipped. This is deliberate: it is the countermeasure to the
  hallucinated-citation failure mode, so do not weaken or bypass the check.
- **Merging a manuscript PR to `main` means "the draft is good", not "submit."** Submission to
  any external venue (arXiv, a conference) is a separate, explicitly human-gated action.
  Nothing in this repo or its CI submits anywhere.
- **`figures/` holds promoted figures only.** Routine per-run plots stay in W&B; a figure
  reaches `benchmark-paper/figures/{direction}/` only when a human, or the Writing agent under
  its manuscript gate, promotes it for a paper. The Writing agent's manuscript-drafting
  workflow is Phase 3 and not yet built — in Phase 1 no agent writes under `benchmark-paper/`
  except Citation to `refs.bib`.
- **Build artifacts are ignored** (`*.aux`, `*.log`, `*.pdf`, `build/`, …). Do not commit a
  compiled PDF; CI attaches it as a build artifact.

## Commands

```bash
cd benchmark-paper && pdflatex main.tex      # local compile (needs a TeX install)
```

There is no local citation-lint command; the check runs in CI on every push and PR. To test
it, open a PR — a `\cite` to a missing key fails `check-citations`.
