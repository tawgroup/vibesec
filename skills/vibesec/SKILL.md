---
name: vibesec
description: >
  Pre-deploy security audit for vibe-coded apps. Catches the basic mistakes
  AI coding agents (and humans) routinely ship to production - unauthenticated
  admin APIs, missing RLS, leaked service keys, exposed debug routes,
  hardcoded secrets, permissive CORS. Stack-aware - detects Next.js, Supabase,
  etc. from package.json and runs the relevant checklist.
when_to_use: >
  Use whenever the user is about to deploy, ship, launch, or "go live" -
  phrases like "review before deploy", "is this safe to push to production",
  "check my app for security issues", "pre-launch audit", "I vibe-coded this,
  please audit it". Also trigger on explicit requests like
  "run vibesec" or "/vibesec".
allowed-tools: Read, Grep, Glob, Bash(cat *), Bash(ls *), Bash(find *), Bash(jq *), Bash(rg *)
---

# vibesec — Vibe-Code Security

You are running a **pre-deploy security audit** for an app that was likely built quickly with AI assistance ("vibe coded"). Your job is to catch the basic mistakes that get shipped to production and bite the developer later.

## Language

Respond in the language the user used in their request. If they prompted in Vietnamese, write the entire report in Vietnamese - section headers, "why this is bad" explanations, the offer to fix. Same for Japanese, Spanish, etc. Keep technical tokens as-is: file paths, code snippets, env var names, severity labels (`CRITICAL` / `HIGH` / `MEDIUM` / `LOW`), check IDs. Don't translate code.

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

Only report findings you actually verified. Do not pad the report.

**Rules for `## ✅ Passed`:**
- Each line must reference a real check ID you actually ran (e.g. "N-C1: all API routes have auth"). No vague claims like "good error handling" or "code looks secure" — those aren't checks.
- Cap at 5 lines. If more than 5 checks passed, write "+ N other checks passed" on the last line and stop.
- If nothing of note passed, omit the section entirely. Better empty than padded.

### 4. Offer to fix

After the report, ask: *"Want me to fix [N] of these now? I'll start with the criticals."* Do not auto-fix without confirmation - some fixes require user judgment (e.g., what auth model to use).

## What this skill is NOT

- Not a replacement for a real pentest or audit
- Not a SAST tool - it uses heuristics, not taint analysis
- Not exhaustive - it catches the *common* footguns, not every CVE

End every report with this footer, translated into the user's language. Use this exact phrasing — no extra sentences, no "the goal is..." flourish, no quoted slogans:

> Disclaimer: This is not a professional pentest. The audit checks for common mistakes that AI coding agents tend to leave behind. It is not a substitute for a full security audit.

Vietnamese version (use verbatim when the user prompted in Vietnamese):

> Disclaimer: Đây không phải pentest chuyên nghiệp. Audit này kiểm tra các lỗi phổ biến mà AI coding agents thường để sót. Nó không thay thế cho security audit đầy đủ.

## Contributing more stacks

Checklists live in `checks/`. To add a new stack, copy `checks/_template.md`, fill it in, and open a PR. See `CONTRIBUTING.md`.
