---
applyTo: 'tests/**'
---

# Pytest suite — guidance

Tests for the `lib/` package. There's no notebook testing here — notebooks
are exploratory; `lib/` is where logic worth testing should live.

## Conventions

- File names: `test_*.py`. Function names: `test_*`. Class names: `Test*`.
- Use `pytest.fixture` for setup; avoid module-level state.
- Use `pytest.parametrize` for table-driven cases — it gives better failure
  messages than a `for` loop with `assert`.
- For expected exceptions use `pytest.raises(...)`, not bare
  `try/except` + `assert False`.

## What's already configured

- `pytest --cov=lib` runs automatically (see `pyproject.toml`). Don't pass
  `--cov` manually unless you're scoping to a single subpath.
- `--strict-markers` and `--strict-config` are on. New custom markers must
  be registered in `pyproject.toml` under `[tool.pytest.ini_options].markers`.
- `--import-mode=importlib` — the test discovery mechanism.

## Hard rules

- **No `sys.path` manipulation in `conftest.py` or anywhere else.** The
  editable install (`uv sync`) puts `lib` on the import path. If imports
  fail, fix the install, not the path.
- **No `pythonpath` key in `[tool.pytest.ini_options]`.** Same reason.
- Tests should run on a fresh checkout after `uv sync` with **no other
  setup**. If you need fixtures from disk, put them under `tests/` and
  load them via `pathlib.Path(__file__).parent / "fixtures" / ...` — never
  read from `data/` in a test (data isn't committed, so it won't exist on
  a fresh clone).

## Things ruff is configured to be lenient about here

The `tests/**/*.py` per-file-ignore in `pyproject.toml` disables `ARG`
(unused args, common in pytest fixtures) and `SIM` (over-eager
simplifications that hurt assertion readability). Don't add `# noqa`
comments for these — they're already allowed.
