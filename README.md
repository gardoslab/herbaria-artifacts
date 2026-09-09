# herbaria-artifacts

The training code the herbaria experiment cycles run, plus everything the agents write that
belongs in git, for the FGVC / extreme-scale / embedding-anomaly project. Formerly
`herbaria-papers`; renamed and split under build-plan T-1.15 of the parent repo
[`herbaria-research-agent-design`](https://github.com/gardoslab/herbaria-research-agent-design).

**Each active research direction gets one workspace on SCC,
`/projectnb/herbdl/workspaces/herb/{direction_id}/`, which is a clone of this repository.**
Jobs run from that checkout. An experiment cycle is the branch `exp/{direction_id}/{cycle_id}`
in that workspace, not a folder; the orchestrator ledger's `runs.git_sha` records the commit
a job was launched from. Run outputs land in `runs/{job_id}/` at the workspace root and are
gitignored.

| Path | Contents | Written by |
|---|---|---|
| `experiments/` | The training code: SWIN/SWINv2 finetuning pipeline, configs, job scripts, sweep launcher, scaling-laws notes. See [`experiments/README.md`](experiments/README.md) and [`experiments/SOURCE.md`](experiments/SOURCE.md). | Experimentation agents, on `exp/{direction_id}/{cycle_id}` branches; humans on `main` |
| `writing/benchmark-paper/` | The benchmark paper: `main.tex`, `refs.bib`, `figures/`. | Writing agent (Phase 3, human-gated), humans |
| `writing/benchmark-paper/refs.bib` | The **only** citation source. | Citation/Literature-Review agent, via PR on `lit/refs-update` — never a direct push to `main` |
| `writing/notebook/{direction}/`, `writing/notebook/digest/` | Per-direction lab notebook entries (one per cycle) and the weekly cross-direction digest. | Writing agent |
| `.github/workflows/latex.yml` | Compiles `writing/**/main.tex` on every push and PR, uploads the PDF, and fails the build if any `\cite` key is missing from `refs.bib`. | — |

Heavy outputs (checkpoints, full training logs, predictions) never land here; they stay on SCC
under `runs/` in the workspace and are referenced by path. Run metrics live in W&B.

## Working here

All changes go on a topic branch and land via pull request; see [`CLAUDE.md`](CLAUDE.md).

```bash
cd writing/benchmark-paper && pdflatex main.tex      # local compile (needs a TeX install)
python3 .github/scripts/check_citations.py          # the same citation lint CI runs
```
