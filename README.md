**🇬🇧 English** • [🇻🇳 Tiếng Việt](./README.vi.md)

# vibesec

> A security audit skill for your app before you deploy. Catch the kind of mistakes you'd really rather not ship to production.

You just vibe-coded an app with Claude / Cursor / Lovable. It works. You're about to deploy. **Before it goes live on the internet**, run this:

```
Audit my app with vibesec
```

You get back something like:

```
# Vibe-Code Security Audit
Stack: Next.js 15 + Supabase
Checks run: 22  •  Issues found: 5 (2 critical, 2 high, 1 medium)

## CRITICAL
1. service_role key exposed in src/lib/admin.ts — anyone can read your DB
2. POST /api/admin/delete-user has no auth — anyone can delete any user
...
```

Then the skill offers to fix them.

## Why this exists

AI coding agents are excellent at shipping features and terrible at security defaults. The recurring vibe-code footguns:

- Admin API routes with no auth check (*"the AI wrote the route, it works, ship it"*)
- Supabase tables with RLS disabled or `USING (true)` policies
- `service_role` key bundled into client-side code
- Authorization based on `user_metadata.role === 'admin'` (user-editable → trivial privilege escalation)
- `.env` committed straight into the repo
- Debug routes (`/api/test`, `/api/seed`) left running in production

This skill encodes that checklist so you don't have to remember it.

## Real-world example

Tested on a real vibe-coded app deployed to Vercel. In 30 seconds it found:

- ✅ 15 API endpoints with no auth check (a flower-shop admin panel)
- ✅ RLS `USING (TRUE)` policies on 8 tables (any authenticated user could read/write/delete anything)
- ✅ Conditional webhook auth instead of mandatory

A simple `curl` confirmed full customer PII (name, phone, email, address, birthday) was returned to anyone on the internet.

## Install

### Option 1: One-liner via `npx skills` (recommended — works across Claude Code, Cursor, Codex, OpenCode...)

```bash
npx skills add the-agents-work/vibesec
```

That's it. Restart your agent and the skill auto-triggers on pre-deploy reviews.

### Option 2: Claude Code plugin marketplace

```
/plugin marketplace add the-agents-work/vibesec
/plugin install vibesec
```

### Option 3: Manual (git clone)

```bash
git clone https://github.com/the-agents-work/vibesec /tmp/vcs-repo
mkdir -p ~/.claude/skills
cp -r /tmp/vcs-repo/skills/vibesec ~/.claude/skills/
```

Restart Claude Code.

## Supported stacks

| Stack | Status |
|---|---|
| Next.js (App Router + Pages Router) | ✅ |
| Supabase | ✅ |
| Common checks (secrets, CORS, headers) | ✅ — runs on every stack |
| Prisma | 🟡 wanted, PR welcome |
| Drizzle | 🟡 wanted, PR welcome |
| SvelteKit | 🟡 wanted, PR welcome |
| Clerk / Auth.js | 🟡 wanted, PR welcome |
| FastAPI | 🟡 wanted, PR welcome |
| Firebase | 🟡 wanted, PR welcome |

Want to add one? See [CONTRIBUTING.md](./CONTRIBUTING.md). Adding a stack is a single markdown file — no code changes.

## How it works

1. Reads `package.json` (and other manifests) to detect your stack
2. Loads the relevant checklist(s) from `checks/`
3. Runs grep / file-pattern checks — **no LLM-as-judge**, every finding points to a real file and line
4. Reports findings grouped by severity (CRITICAL / HIGH / MEDIUM / LOW)
5. Asks before fixing anything

## What this is NOT

- Not a replacement for a real pentest
- Not a SAST tool with taint analysis
- Not exhaustive — it catches *common footguns*, not every CVE

The goal: **you won't ship the obvious mistakes**. That's worth a lot when the alternative is finding out at 2am that anon can delete any user.

## License

MIT. Fork it, improve it, ship it.

## Credits

Built by [@toanbku](https://github.com/toanbku) for the global vibe-coding community.
