# Provenance of `experiments/`

The code in this subtree was **imported from
[`gardoslab/herbdl`](https://github.com/gardoslab/herbdl), branch `agent-research-pipeline`,
commit `bf8dfcc7ff698a540c599e5dde7c8244f3eeb29e`, on 2026-09-09.**

It was copied, not merged: no git history came across, so this file is the record of where
it came from. `herbdl` was not modified by the import.

## Why the code lives here now

Each research direction's SCC workspace, `/projectnb/herbdl/workspaces/herb/{direction_id}/`,
is a clone of *this* repository, and jobs are submitted from that checkout. The training code
therefore has to be in this repo for a cycle branch to be runnable. See
[`README.md`](README.md).

## What was copied

| Destination | Source in `herbdl` | Size | Notes |
|---|---|---|---|
| `finetuning/SWIN/` | `finetuning/SWIN/` | ~800K | Direction A: the SWIN / SWINv2 finetuning pipeline — `SWIN_finetuning.py`, `SWIN_finetuning_advanced.py`, `configs/`, `configs_advanced/`, `hyperparameter_configs/`, `launch_sweep.py`, prediction and Kaggle-submission scripts, SGE `submit_*.sh` / `train*.sh`, `PLOTS/` per-run summary text files, and the markdown design docs. |
| `finetuning/SWIN-CLIP/` | `finetuning/SWIN-CLIP/` | ~60K | Minus `playground.ipynb` (see below). |
| `finetuning/BioCLIP/` | `finetuning/BioCLIP/` | ~16K | |
| `finetuning/__init__.py`, `finetuning/requirements.txt` | same | — | The minimal `torch`/`torchvision`/`datasets` pins that shipped with `finetuning/`. |
| `scaling-laws/` | `scaling-laws/` | ~8K | Direction B notes and ledger (`notes.md`, `ledger.md`). No code. |
| `requirements.txt` | `herbdl` top-level `requirements.txt` | ~4K | Copied because it differs substantially from `finetuning/requirements.txt`: 145 fully pinned packages versus 3 loose ones. This is the reference for the SCC `herb_env` conda environment. |

Total added: about 900 KB. No file exceeds 2 MB; the largest is
`finetuning/SWIN/metric_explore.ipynb` at 108 KB, which is kept because it is part of the
SWIN evaluation pipeline.

## No top-level `herbdl` modules were needed

`herbdl`'s top-level packages (`utils/`, `dataset_utils/`, `datasets/`, `CLIP/`) are **not**
imported by anything under `finetuning/` or `scaling-laws/`, so none were copied. Two
imports look like they might be and are not:

- `from datasets import load_dataset` is the Hugging Face `datasets` library, not `herbdl/datasets/`
  (which defines no `load_dataset`).
- `from utils import ImageDatasetTrain` in `finetuning/SWIN-CLIP/*.py` resolves to the sibling
  `finetuning/SWIN-CLIP/utils.py`, not `herbdl/utils/`.

`scaling-laws/` contains no Python at all.

## What was deliberately left behind

- **`finetuning/CLIP archive/`** (~16 MB) — an archive of superseded CLIP notebooks
  (`CLIP_explain.ipynb`, `evaluation.ipynb`, `evaluation copy.ipynb`, `plots.ipynb`, …). Bulk,
  not pipeline; it stays in `herbdl`.
- **`finetuning/SWIN-CLIP/playground.ipynb`** (2.4 MB) — over the 2 MB ceiling, and scratch
  rather than pipeline.
- **`finetuning/output/`** — a run-output directory. Run outputs now live in the workspace's
  gitignored `runs/{job_id}/`.
- **`finetuning/venv/`, any `wandb/` directory, `__pycache__/`, `.DS_Store`** — environment and
  scratch.
- **`finetuning/.gitignore` and `finetuning/SWIN-CLIP/.gitignore`** — deliberately not copied.
  They carry `herbdl`-specific patterns (`PLOTS/`, `*.o*`, `*.e*`, `dataset_explore.ipynb`)
  that would have ignored files this import is bringing in, notably `SWIN/PLOTS/`. This
  repository's root `.gitignore` is the single authority.
- **`finetuning/CLAUDE.md`** — a three-line `herbdl` note that would otherwise be picked up as
  agent instructions for *this* repository. Its one substantive fact, that these scripts run
  under the `herb_env` conda environment on SCC, is recorded in [`README.md`](README.md)
  instead.
- **Everything else at `herbdl`'s top level** — `clustering_viz/`, `datasets/`,
  `dataset_utils/`, `descriptions/`, `interpretability/`, `utils/`, `CLIP/`, `docs/`,
  `agent-orchestrator/`, `.claude/`, `AGENTS.md`, `AGENT_RESEARCH.md`, `CLAUDE.md`,
  `README.md`, `LICENSE`.

## `herbdl` remains the archive

`herbdl` is still the home for exploration notebooks and for the clustering and visualization
work (`clustering_viz/`, `interpretability/`, `descriptions/`, the dataset-construction
utilities). This repository holds only the code an experiment cycle runs. Import further code
the same way — copy it, and extend this file.
