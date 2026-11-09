# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability in this project, **please do not
open a public GitHub issue**. Public issues are visible to everyone and may
give attackers a head start.

Instead, use GitHub's *Private Vulnerability Reporting* feature:

- [Report a vulnerability](https://github.com/BenFlint123/uv_ruff_ds_template/security/advisories/new)

This creates a private draft advisory visible only to maintainers until a
fix is coordinated.

## What to include in a report

To help triage quickly, please include where possible:

- A description of the vulnerability and its potential impact.
- The affected commit SHA.
- Steps to reproduce, or a minimal proof-of-concept.
- Any suggested mitigation.

## Scope

This policy covers vulnerabilities in:

- The `lib` package source (`lib/`).
- The CI/CD configuration in this repository.

This project doesn't follow a versioned release process or serve traffic —
most findings will relate to dependency vulnerabilities or CI/tooling
misconfiguration. Issues in third-party dependencies should be reported
upstream to the relevant project; please still let us know so we can pin a
fixed version.
