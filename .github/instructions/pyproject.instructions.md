---
applyTo: 'pyproject.toml'
---

# pyproject.toml — guidance

This file is the **single source of truth** for build, dependencies, and
tool configuration. Don't split things into separate config files
(`.flake8`, `pytest.ini`, `setup.cfg`) — keep them all here.

## Dependencies

- **Analysis deps** (pandas, numpy, matplotlib, scikit-learn, ...) go in
  `[project].dependencies`. Add them as the project actually needs them —
  don't pre-install a generic DS stack "just in case".
- **Dev/tooling deps** go in `[dependency-groups]` (uv-native). Install with
  `uv sync --all-groups` or scoped to a group with `uv sync --group dev`.
- Use lower bounds (`>=X.Y`), not exact pins, in this file. The exact
  resolution lives in `uv.lock` — that's what's installed reproducibly.
- **No `requirements.txt`.** If a downstream consumer asks for one, generate
  it on the fly with `uv export -o requirements.txt`.
- Pulling in another internally-released package (no PyPI needed): `uv add
  "pkgname @ git+https://github.com/org/repo.git@vX.Y.Z"`. See the README
  for details.

## Tool configuration

- `[tool.ruff]` — `target-version = "py311"`, `line-length = 88`. No
  docstring rule enabled (`D1` is intentionally not selected) — notebooks
  and exploratory code shouldn't be blocked on missing docstrings.
- `[tool.pytest.ini_options]` — **no `pythonpath` key**. The editable
  install handles imports.
- `[tool.coverage.run]` — `branch = true`. **Don't add `--cov-fail-under`**
  — coverage is reported, not gated, by deliberate choice.

## Build

- Build backend is `hatchling`, but only to make `uv sync` install `lib` in
  editable mode. There's no sdist curation, no `py.typed` marker, no
  publishing — this project isn't meant to be distributed.

## Version

- `[project].version` exists because `pyproject.toml` requires it, not
  because this project follows a release process. There's no
  `__version__` machinery to keep in sync and no CHANGELOG — bump it only
  if you have a specific reason to.
