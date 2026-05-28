---
name: vibe-code-security
description: Pre-deploy security audit for vibe-coded apps. Catches the basic mistakes AI coding agents (and humans) routinely ship to production - unauthenticated admin APIs, missing RLS, leaked service keys, exposed debug routes, hardcoded secrets, permissive CORS. Stack-aware: detects Next.js, Supabase, etc. from package.json and runs the relevant checklist.
when_to_use: Use whenever the user is about to deploy, ship, launch, or "go live" - phrases like "review before deploy", "is this safe to push to production", "check my app for security issues", "pre-launch audit", "I vibe-coded this, please audit it". Also trigger on explicit requests like "run vibe-code-security" or "/vibe-code-security".
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(ls *), Bash(find *), Bash(jq *), Bash(rg *)
---

# vibe-code-security

You are running a **pre-deploy security audit** for an app that was likely built quickly with AI assistance ("vibe coded"). Your job is to catch the basic mistakes that get shipped to production and bite the developer later.

## Audit flow

Follow these steps in order. Do NOT skip detection - running the wrong checklist wastes the user's time.

### 1. Detect the stack

Read `package.json` (and `pnpm-workspace.yaml` / `pyproject.toml` / `Cargo.toml` / `go.mod` if present) to identify what's in use. Map dependencies to checklists:

| Dependency signal | Load checklist |
|---|---|
| `next` in dependencies | `checks/nextjs.md` |
| `@supabase/*` in dependencies | `checks/supabase.md` |
| (always) | `checks/common.md` |

If no `package.json` exists, look for other markers (`supabase/` directory, `.env.example`, etc.). If the stack is unrecognized, tell the user which stacks are currently supported and offer to run only `checks/common.md`.

### 2. Run the checklists

For each loaded checklist, perform every check it lists. Use `Grep`/`Glob`/`Read` - do NOT make up findings. Every reported issue must point to a real file and line.

### 3. Report

Output a single markdown report grouped by severity:

```
# Vibe-Code Security Audit

**Stack detected:** Next.js 15 + Supabase
**Checks run:** 18  •  **Issues found:** 4 (1 critical, 2 high, 1 medium)

## CRITICAL
### 1. service_role key exposed to client
**File:** `src/lib/supabase-admin.ts:3`
**Why this is bad:** The service_role key bypasses RLS entirely. Anyone who opens DevTools can read or modify any row in your database.
**Fix:**
\`\`\`ts
// Move this file to a Server Component / Route Handler only.
// Never import it from a "use client" file or anything reachable from the browser bundle.
\`\`\`

## HIGH
...

## MEDIUM
...

## ✅ Passed
- RLS enabled on all tables
- No hardcoded API keys in src/
- ...
```

**Severity rules:**
- **CRITICAL** = attacker can exploit immediately with no special access (e.g., service_role key in client bundle, admin API with no auth)
- **HIGH** = exploitable with minimal effort (e.g., RLS off, debug route accessible in prod build)
- **MEDIUM** = bad practice or defense-in-depth gap (e.g., missing security headers, open CORS for non-auth endpoints)
- **LOW** = nitpick, only mention if relevant

Only report findings you actually verified. If a check passes, list it under "Passed" so the user sees what was covered. Do not pad the report.

### 4. Offer to fix

After the report, ask: *"Want me to fix [N] of these now? I'll start with the criticals."* Do not auto-fix without confirmation - some fixes require user judgment (e.g., what auth model to use).

## What this skill is NOT

- Not a replacement for a real pentest or audit
- Not a SAST tool - it uses heuristics, not taint analysis
- Not exhaustive - it catches the *common* footguns, not every CVE

Tell the user this explicitly in the report footer. The goal is "you won't ship the obvious mistakes," not "your app is bulletproof."

## Contributing more stacks

Checklists live in `checks/`. To add a new stack, copy `checks/_template.md`, fill it in, and open a PR. See `CONTRIBUTING.md`.
