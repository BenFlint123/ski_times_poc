# uv_ruff_ds_template

A lightweight scaffold for data-science work: `uv` + Ruff + Jupyter,
structured so you can clone this, get a dataset, and start working
immediately.

> **Status:** Template scaffold. `lib/` is a stub for whatever reusable
> code you like to bring into your analysis — add modules to it as
> patterns emerge from your notebooks. Leave the name as-is unless you'd
> prefer something more specific.

---

## Using this template

How you acquire the template depends on whether you're free to create the
destination repo yourself, or your org requires it to be created some
other way first (e.g. through an internal portal), which usually means it
already exists with its own initial commit before you get to it.

**If you can create the destination repo directly:** use GitHub's "Use
this template" button, or:

```powershell
gh repo create my-project --template BenFlint123/uv_ruff_ds_template --clone
cd my-project
```

**If the destination repo already exists** (so "Use this template" can't
target it), import the template's files with a squash-merge instead —
this pulls in the current file contents as a single clean commit, without
importing the template's own commit history:

```powershell
git clone <your-new-repo-url>
cd <your-new-repo>
git remote add template https://github.com/BenFlint123/uv_ruff_ds_template.git
git fetch template
git checkout -b add-template-scaffold
git merge --squash --allow-unrelated-histories template/main
```

This will likely conflict on files your repo already has (commonly
`README.md` and `.gitignore`, if it was created with either). Check
`git status` for the conflicted files, open each one, and — assuming you
want the template's version — resolve it with:

```powershell
git checkout --theirs <path>
git add <path>
```

Then commit, push the branch, and open a pull request into your default
branch so CI runs on it before you merge:

```powershell
git commit -m "Add data-science project scaffold from template"
git push -u origin add-template-scaffold
```

**Either way, once you have the template's files in your repo**, work
through this checklist before adding your own code:

1. **Pick a package name** (PEP 8: lowercase, ideally one word) — or leave
   it as `lib`; it's generic on purpose and doesn't need renaming. If you
   do rename, global-replace `lib` across the workspace, including:
   - the directory `lib/`
   - `pyproject.toml` (`name`, hatch `packages`, ruff `src` /
     `known-first-party`, `--cov=…`, `coverage.run.source`)
   - `tests/test_smoke.py`
   - `.github/copilot-instructions.md`, `.github/instructions/*.md`
   - `.pre-commit-config.yaml` (`files:` patterns)
   - `README.md` and `CONTRIBUTING.md` prose references
2. **Set the project name and description** in `README.md` (the title and
   the `cd <repo>` line in the clone snippet) and `pyproject.toml`
   (`description`).
3. **Update the repository URL** in `pyproject.toml` (`[project.urls]
   Repository`), `.github/ISSUE_TEMPLATE/config.yml` (both `url:` fields),
   and `SECURITY.md` (the "Report a vulnerability" link).
4. **Review `LICENSE`**, **`.github/CODEOWNERS`**, and the `authors` field
   in `pyproject.toml` — update the copyright holder / owner if this isn't
   your project.
5. Run `uv sync --all-groups` to generate a fresh `uv.lock`.

---

## Quick start

This project uses [`uv`](https://docs.astral.sh/uv/) to manage the Python
toolchain, virtual environment and dependencies. You do **not** need a
system-wide Python 3.11 — `uv` will fetch one for you.

```powershell
# 1. Install uv (one-time, if you don't have it):
#    https://docs.astral.sh/uv/getting-started/installation/

# 2. Clone & enter the repo
git clone <your-repo-url>
cd uv_ruff_ds_template

# 3. Install Python 3.11 (managed by uv) and pin the project to it
uv python install 3.11
uv python pin 3.11

# 4. Create the venv and install the project + dev dependencies
uv venv
uv sync --all-groups

# 5. Install pre-commit hooks
uv run pre-commit install
uv run pre-commit install --hook-type pre-push
```

Verify the install:

```powershell
uv run python -c "import lib; print('lib import OK')"
uv run pytest -q
uv run jupyter lab
```

Drop your dataset into `data/raw/`, open a notebook under `notebooks/`, and
`import lib` works immediately — no extra setup.

## Project structure & workflow

```
data/
├── raw/         # dataset exactly as received — never edited in place
├── interim/     # working intermediate outputs
└── processed/   # final, analysis-ready data notebooks actually read from
notebooks/       # exploration, numbered by topic (01_explore.ipynb, ...)
lib/              # reusable code shared across notebooks (stub package)
tests/            # tests for lib/
```

- **`data/`** — all three subfolders are gitignored except a `.gitkeep`
  marker, so the folders exist after a fresh clone but no data is ever
  committed. `raw/` is the dataset untouched; `interim/` holds your working
  intermediate outputs; `processed/` is what your notebooks should actually
  read from for analysis.
- **`notebooks/`** — exploratory work. Name files with a numeric prefix
  (`01_explore.ipynb`) so the investigation order is visible in the file
  list. `nbstripout` strips cell outputs automatically before each commit,
  keeping diffs readable.
- **`lib/`** — anything you end up reusing across more than one notebook:
  data loading, cleaning, data-quality checks, plotting helpers. For
  example, a function in `lib/dq.py` is used from any notebook via:
  ```python
  from lib.dq import check_missing_rates
  ```
  This works with no `sys.path` setup because `uv sync` installs `lib` in
  editable mode — the same mechanism in VS Code, plain `jupyter lab`,
  scripts, and pytest.
- **`tests/`** — tests for `lib/` code, not the notebooks themselves.

Need to pull in another project of yours that's already packaged and
released (not on PyPI)? No PyPI required — `uv` installs directly from git:
```powershell
uv add "pkgname @ git+https://github.com/org/repo.git@vX.Y.Z"
```

## Day-to-day commands

```powershell
uv run pytest                     # run tests for lib/ + coverage report
uv run ruff format .              # format
uv run ruff check . --fix         # lint + autofix
uv run pre-commit run --all-files # all commit-stage hooks
uv run jupyter lab                # start notebook server
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

BSD 3-Clause — see [LICENSE](LICENSE).
