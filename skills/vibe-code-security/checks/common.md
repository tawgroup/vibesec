# Common checks (run on every stack)

Run every check below. For each, report findings under the right severity. Cite file + line.

---

## CRITICAL

### C-C1. Secrets committed to git
**Look for:**
- `.env`, `.env.local`, `.env.production` tracked by git: `git ls-files | grep -E '\.env($|\.)'`
- Hardcoded API keys in source: grep for high-entropy patterns. Common prefixes:
  - `sk-` (OpenAI, Anthropic)
  - `sk_live_`, `sk_test_` (Stripe)
  - `eyJ...` long strings (JWT)
  - `xoxb-`, `xoxp-` (Slack)
  - `ghp_`, `gho_`, `ghu_` (GitHub)
  - `AIza` (Google API)
  - `AKIA` (AWS access key)

**Why this is bad:** Git history is forever. Even after rotation, the old key sits in history and shows up in scrapers.
**Fix:** Rotate the key NOW, then `git rm --cached`, add to `.gitignore`, force-push only if you understand the implications (or just rotate and move on).

### C-C2. `.env` not in `.gitignore`
**Look for:** Read `.gitignore`. Confirm it excludes `.env`, `.env.local`, `.env.*.local`.

---

## HIGH

### C-H1. Hardcoded secrets in source files
**Look for:** Same prefixes as C-C1, but checking source files even if not committed. Sometimes the file is gitignored but the secret leaks via build artifacts or shared screenshots.

### C-H2. `console.log` of sensitive values
**Look for:** `grep -rn "console\.\(log\|debug\|info\)" --include="*.ts" --include="*.tsx" --include="*.js"` then scan for variables named `token`, `password`, `secret`, `key`, `apiKey`, `user`, `session`.
**Why this is bad:** Logs end up in Vercel/CloudWatch/Sentry. Production logs with PII = compliance risk.

### C-H3. Open CORS on credentialed endpoints
**Look for:** Headers setting `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true`. This combination is actually rejected by browsers, but the *intent* signals a misunderstanding worth flagging - the developer probably wanted to allow specific origins.

### C-H4. Outdated dependencies with known CVEs
**Action:** Run `npm audit --production` (or `pnpm audit`, `yarn audit`). Report only `high` and `critical` from the output. Skip dev-only vulns.

---

## MEDIUM

### C-M1. Missing security headers
**Look for:** Config for `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`. Per-stack config location:
- Next.js: `next.config.*` headers()
- Vercel: `vercel.json` headers
- Express: `helmet` middleware

### C-M2. CSP missing or set to `unsafe-inline unsafe-eval`
**Why this is bad:** CSP is the strongest defense against XSS. `unsafe-inline` for scripts defeats most of its value.

### C-M3. Sensitive data in URL query params
**Look for:** `?token=`, `?key=`, `?password=`, `?email=` in routes / redirects / fetch URLs.
**Why this is bad:** URLs end up in browser history, server logs, referrer headers.

---

## LOW

### C-L1. `robots.txt` missing in `public/`
### C-L2. No `SECURITY.md` for the repo (responsible disclosure path)
### C-L3. Dependabot / Renovate not configured
