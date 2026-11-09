---
applyTo: '.github/workflows/**'
---

# GitHub Actions workflows — guidance

## Pinning

- **First-party GitHub actions** (`actions/*`, `github/*`): pin to a major
  tag (e.g., `actions/checkout@v4`). These are lower supply-chain risk and the
  tag is treated as a moving "latest minor/patch within v4" pointer.
- **Third-party actions**: pin to an **immutable commit SHA** with the
  human-readable version in a trailing comment, e.g.,

  ```yaml
  uses: astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b # v8.1.0
  ```

  Where the action also takes a tool version as input (`astral-sh/setup-uv` with
  `with: { version: "0.9.26" }`), keep that pin too — it's defence-in-depth on the
  binary the action installs.
- Dependabot (`.github/dependabot.yml`) will open PRs to bump these — let
  it do the work rather than chasing latest manually.
- Some actions (e.g. `astral-sh/setup-uv` from v8.0.0) now publish
  GitHub-immutable releases, so the `@vX.Y.Z` tag itself can't be
  re-pointed. We still pin to the SHA: it's defence-in-depth, and
  CodeQL's `actions/unpinned-tag` query doesn't yet recognise immutable
  tags as safe.

## CI job

- CI runs as a single job on `ubuntu-latest` / Python 3.11 — there's no
  matrix. This is a local analysis project, not a cross-platform library;
  one environment is the one that matters. If cross-platform or
  multi-version behaviour ever becomes a real concern, add a matrix then,
  gating OS/version-independent steps with `if:` so they only run once.

## Concurrency

- Workflow-level `concurrency:` block cancels superseded runs on the same
  branch — don't remove it without a reason. Saves Actions minutes during
  rapid iteration.

## Don't add

- **Step-level `continue-on-error: true`** to "make CI green". That's how
  silent regressions land. If a check is genuinely flaky, fix the flake.
- **Caching beyond `astral-sh/setup-uv`'s built-in cache.** uv's cache is
  already enabled via `enable-cache: true`. A separate `actions/cache@v4`
  step on top is redundant and easy to misconfigure.
- **Secrets in PR-triggered workflows from forks.** GitHub blocks this for
  good reason; don't try to work around it.

## When adding a new check

- Run it locally first via `uv run <tool>` to confirm the command form
  before wiring it into CI.
- Make it required in branch protection only after it's proven stable.
