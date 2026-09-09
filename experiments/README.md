# experiments/

The training code the herbaria experiment cycles actually run. Framework doc §8.1 (parent
repo `herbaria-research-agent-design`); made concrete by build-plan T-1.14/T-1.15.

This subtree is **code, not per-cycle folders**. There is no `{direction}/{cycle}/` layout —
a cycle is a *branch*, not a directory.

## The workspace model

Each active research direction gets one workspace on SCC:

```
/projectnb/herbdl/workspaces/herb/{direction_id}/
```

That workspace is a **git clone of this repository**. `{direction_id}` matches the `id`
field of the direction's YAML in `herbaria-orchestrator/directions/`. A job submitted for
that direction runs from that checkout, so everything the job needs — training scripts, job
scripts, configs — has to live in this subtree.

## A cycle is a branch

An experiment cycle `{cycle_id}` is the branch `exp/{direction_id}/{cycle_id}`, checked out
in that direction's workspace. On it the Experimentation agent commits the changes the cycle
proposes: config edits, job-script changes, new or modified training/eval scripts.

The orchestrator ledger records the link back: `runs.git_sha` is the commit the job was
actually launched from. A run is therefore always reproducible from a commit in this repo,
and `runs.git_sha` — not a folder name — is what ties a W&B run to its code.

Reaching `main` is a **human pull request**. An agent never merges its own cycle branch.

## Run outputs are not committed

Checkpoints, full training logs, predictions and W&B scratch go to

```
{workspace}/runs/{job_id}/
```

— `runs/` at the repo root of the workspace, gitignored (see the root `.gitignore`). They
stay on SCC and are referenced by path from the ledger and from the cycle's finding. Metrics
live in W&B.

Small evaluation outputs — a metrics JSON, a per-class table, a modest plot — **may** be
committed on the cycle branch, next to the code that produced them.

## Rules

- **Small files only.** If a file is more than a few MB, it does not belong in git.
  Checkpoints, arrow shards, full prediction dumps and image data stay under `runs/` or
  elsewhere on SCC and are referenced by path.
- **Written on a cycle branch, never on `main`.** The Experimentation agent commits only to
  `exp/{direction_id}/{cycle_id}`, and only under `experiments/`. It never writes under
  `writing/`.
- **Reusable software is not a special case.** A new sampler or metric utility lands on the
  cycle branch first and becomes shared code on `main` only through a human PR.
- **Nothing here is a citation source.** Manuscripts under `writing/` cite only
  `writing/benchmark-paper/refs.bib`; a figure moves from a cycle's eval output (or W&B)
  into `writing/<paper>/figures/` only when a human or the Writing agent promotes it.

## What is here

| Path | Contents |
|---|---|
| `finetuning/SWIN/` | The SWIN/SWINv2 finetuning pipeline — Direction A. Training entry points, configs, sweep launcher, prediction and Kaggle submission scripts, SGE job scripts. |
| `finetuning/SWIN-CLIP/`, `finetuning/BioCLIP/` | Related finetuning variants. |
| `finetuning/requirements.txt` | The minimal torch/torchvision/datasets pins that shipped with `finetuning/`. |
| `scaling-laws/` | Direction B notes and ledger. |
| `requirements.txt` | The full pinned environment from the source repo. |
| `SOURCE.md` | Provenance: where this code was imported from and what was left behind. |

Scripts under `finetuning/` were developed against the `herb_env` conda environment on SCC
(`conda activate herb_env`); the pinned `requirements.txt` here is the reference for what
that environment contains.
