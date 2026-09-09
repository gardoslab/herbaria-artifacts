# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## What this repo is

The git home for the herbaria research team's training code and for the writing material
(manuscripts, papers, lab notebook) its agents produce. Formerly `herbaria-papers`; renamed
and split under build-plan T-1.15. It is a **submodule** of
`gardoslab/herbaria-research-agent-design`, which holds the governing documents
(`herbaria-agent-framework-v2.md`, `herbaria-build-plan-v2.md`); the agent code that writes
into this repo lives in the sibling submodule `gardoslab/herbaria-orchestrator`.

**This repo is also what runs on the cluster.** Each active research direction gets one SCC
workspace, `/projectnb/herbdl/workspaces/herb/{direction_id}/`, which is a **clone of this
repository**; jobs are submitted from that checkout, which is why the training code lives
here. An experiment cycle is a **branch**, `exp/{direction_id}/{cycle_id}`, not a folder —
there is no per-cycle directory layout. The orchestrator ledger's `runs.git_sha` records the
commit a job ran from. Run outputs go to `runs/{job_id}/` at the workspace root and are
gitignored; they are never committed.

| Path | Contents |
|---|---|
| `experiments/` | The training code a cycle runs and edits: the SWIN/SWINv2 finetuning pipeline, configs, SGE job scripts, sweep launcher, scaling-laws notes. Model and rules in `experiments/README.md`; provenance in `experiments/SOURCE.md`. |
| `writing/benchmark-paper/main.tex` | The benchmark paper. Compiles locally with `pdflatex main.tex`. |
| `writing/benchmark-paper/refs.bib` | The **only** citation source. Owned by the Citation/Literature-Review agent. |
| `writing/benchmark-paper/figures/` | Promoted figures only, in per-direction subfolders. |
| `writing/notebook/{direction}/`, `writing/notebook/digest/` | Lab notebook: one entry per cycle per direction, plus the weekly cross-direction digest. Owned by the Writing agent. |
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

Agent-owned branches follow their own naming, enforced by the orchestrator: Experimentation
writes on `exp/{direction_id}/{cycle_id}` and Citation on `lit/refs-update`. Do not reuse those
prefixes for human work.

If you find uncommitted changes already sitting on `main` or a detached HEAD, leave them
uncommitted.

## Rules specific to this repo

These are the human gates from the framework doc (§6.2, §7, §8.1); the agents enforce them
structurally and a human editing by hand should hold to the same lines.

- **Each subtree has one kind of writer.** `experiments/` is written by that direction's
  Experimentation agent, only on that cycle's branch `exp/{direction_id}/{cycle_id}`, and
  nowhere else — it never writes under `writing/`. Its run outputs go to `runs/{job_id}/` in
  the SCC workspace, which is local to that clone and never committed. `writing/notebook/` is
  written by the Writing agent. `writing/<paper>/` is written by humans and, in Phase 3, by
  the Writing agent under its manuscript gate. No agent writes outside its subtree; the
  orchestrator's scoping tests assert this.
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
- **`figures/` holds promoted figures only.** Routine per-cycle plots stay in W&B or on the
  cycle branch; a figure reaches `writing/<paper>/figures/{direction}/` only when a human, or
  the Writing agent under its manuscript gate, promotes it for a paper.
- **Small files only under `experiments/`.** Checkpoints, full logs and predictions stay on
  SCC under the workspace's gitignored `runs/{job_id}/` and are referenced by path. Anything
  over a few MB does not belong in git. Small eval outputs (a metrics JSON, a per-class
  table) may be committed on the cycle branch.
- **Build and run artifacts are ignored** — LaTeX output under `writing/` (`*.aux`, `*.log`,
  `*.pdf`, `build/`, …), and `runs/`, `**/output/`, `**/wandb/`, model weights, virtualenvs
  and SGE job logs anywhere. Do not commit a compiled PDF; CI attaches it as a build
  artifact. Note the LaTeX patterns are scoped to `writing/` on purpose, so that `*.log` and
  `*.out` remain committable eval outputs under `experiments/`.

## Commands

```bash
cd writing/benchmark-paper && pdflatex main.tex      # local compile (needs a TeX install)
python3 .github/scripts/check_citations.py          # the citation lint, same as CI
```
