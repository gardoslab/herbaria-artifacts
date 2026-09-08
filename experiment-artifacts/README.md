# experiment-artifacts/

The git home for everything an experiment cycle produces that belongs in version control.
Framework doc §8.1 (parent repo `herbaria-research-agent-design`); made concrete by build-plan
T-1.14/T-1.15.

## Layout

```
experiment-artifacts/
  {direction_id}/
    {cycle_id}/
      configs/        # training / sweep configs the cycle proposed or was seeded with
      jobs/           # SGE job scripts as submitted (smoketest and full run)
      eval/           # small evaluation outputs: metrics JSON, per-class tables, plots
      scripts/        # any script or utility the Experimentation agent wrote for this cycle
      README.md       # written by the cycle: proposal ref, W&B run ids, SCC run_dir, git SHA
```

`{direction_id}` matches the `id` field of the direction's YAML in
`herbaria-orchestrator/directions/`; `{cycle_id}` is the ledger `cycles` row id.

## Rules

- **Written on a per-cycle branch, never on `main`.** An Experimentation agent commits to
  `exp/{direction_id}/{cycle_id}` and only under its own `{direction_id}/{cycle_id}/` folder.
  Reaching `main` is a human-reviewed pull request.
- **Small things only.** Checkpoints, full training logs and predictions stay on SCC under
  `$RUN_ROOT/{direction_id}/{cycle_id}/{job_id}/` and are referenced by path from the ledger
  and from the cycle's `README.md`. Metrics live in W&B. If a file is more than a few MB, it
  does not belong here.
- **Reusable software is not a special case.** A new sampler or metric utility lands in the
  cycle's `scripts/` first and becomes shared code only through a human PR — to this repo's
  `main`, or to the training codebase if that is where it belongs.
- **Nothing here is a citation source.** Manuscripts under `writing/` cite only
  `writing/benchmark-paper/refs.bib`; figures move from a cycle's `eval/` (or W&B) into
  `writing/<paper>/figures/` only when a human or the Writing agent promotes them.
