---
applyTo: 'notebooks/**'
---

# Notebooks — guidance

`notebooks/` is for exploration: understanding a dataset, trying an
approach, producing a result. It is not where reusable code should live.

## Conventions

- Name notebooks with a numeric prefix + topic, e.g. `01_explore.ipynb`,
  `02_feature_checks.ipynb`. The prefix reflects the order of
  investigation, not a strict pipeline stage.
- Import shared logic from `lib/` rather than redefining it in a cell —
  `from lib.dq import check_missing_rates`. If a function starts getting
  copy-pasted across notebooks, that's the signal to move it into `lib/`.
- Read from and write to `data/` using the `raw/` → `interim/` →
  `processed/` convention — never overwrite `data/raw/`.
- Before committing, **Restart & Run All** so the notebook reflects a clean
  execution, not leftover state from out-of-order cell runs.
- `nbstripout` strips cell outputs automatically at commit time — don't
  fight it by re-adding outputs or disabling the hook. If you need to
  share a rendered result, export it (e.g. to `data/processed/` or a
  markdown summary) rather than committing notebook output cells.

## What's already set up

- `import lib` (and submodules) works out of the box — no `sys.path`
  hacks needed, in VS Code or plain `jupyter lab`. This relies on the
  editable install from `uv sync`; if it stops working, run `uv sync`
  again rather than adding a path workaround.
- `ipykernel` and `jupyterlab` are already in the `dev` dependency group.
