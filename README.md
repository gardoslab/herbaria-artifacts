# herbaria-artifacts

Everything the herbaria research team's agents produce that belongs in git — experiment
artifacts and writing material — for the FGVC / extreme-scale / embedding-anomaly project.
Formerly `herbaria-papers`; renamed and split under build-plan T-1.15 of the parent repo
[`herbaria-research-agent-design`](https://github.com/gardoslab/herbaria-research-agent-design).

| Path | Contents | Written by |
|---|---|---|
| `experiment-artifacts/{direction}/{cycle}/` | Configs, job scripts, small eval outputs and scripts from each experiment cycle. See [`experiment-artifacts/README.md`](experiment-artifacts/README.md). | Experimentation agents, on `exp/{direction}/{cycle}` branches |
| `writing/benchmark-paper/` | The benchmark paper: `main.tex`, `refs.bib`, `figures/`. | Writing agent (Phase 3, human-gated), humans |
| `writing/benchmark-paper/refs.bib` | The **only** citation source. | Citation/Literature-Review agent, via PR on `lit/refs-update` — never a direct push to `main` |
| `writing/notebook/{direction}/`, `writing/notebook/digest/` | Per-direction lab notebook entries (one per cycle) and the weekly cross-direction digest. | Writing agent |
| `.github/workflows/latex.yml` | Compiles `writing/**/main.tex` on every push and PR, uploads the PDF, and fails the build if any `\cite` key is missing from `refs.bib`. | — |

Heavy outputs (checkpoints, full training logs, predictions) never land here; they stay on SCC
storage and are referenced by path. Run metrics live in W&B.

## Working here

All changes go on a topic branch and land via pull request; see [`CLAUDE.md`](CLAUDE.md).

```bash
cd writing/benchmark-paper && pdflatex main.tex      # local compile (needs a TeX install)
python3 .github/scripts/check_citations.py          # the same citation lint CI runs
```
