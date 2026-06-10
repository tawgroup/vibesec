# Security Policy

vibesec is a static checklist skill — plain markdown, no executable code, no network calls, no database connections. The attack surface is small, but mistakes in the checklists themselves can still cause harm: a fix template that introduces a bug, or a check that gives false confidence about a real vulnerability.

## Reporting

- **Wrong or harmful fix template / check that misses what it claims to catch:** open a regular [GitHub issue](https://github.com/tawgroup/vibesec/issues). The checklists are public docs — discussing them publicly is fine and helps everyone.
- **Something sensitive** (e.g. a way the skill could be abused, prompt-injection via a scanned repo that hijacks the audit): use [GitHub private vulnerability reporting](https://github.com/tawgroup/vibesec/security/advisories/new) on this repo.

We aim to respond within 7 days.

## Scope notes

vibesec audits *other* projects. Findings it produces about your app are your responsibility to triage — see the disclaimer in every report: it is not a pentest and not a substitute for a full security audit.
