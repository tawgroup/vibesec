**🇬🇧 English** • [🇻🇳 Tiếng Việt](./README.vi.md)

# vibe-code-security

> A Claude Code skill that audits your vibe-coded app for the basic security mistakes you'd be embarrassed to ship.

You built something in a weekend with Claude / Cursor / Lovable. It works. You're about to deploy. **Before you tweet the launch**, run this:

```
Please audit my app with vibe-code-security
```

You get a report like:

```
# Vibe-Code Security Audit
Stack detected: Next.js 15 + Supabase
Checks run: 22  •  Issues found: 5 (2 critical, 2 high, 1 medium)

## CRITICAL
1. service_role key exposed in src/lib/admin.ts — anyone can read your DB
2. POST /api/admin/delete-user has no auth — anyone can delete any user
...
```

Then it offers to fix them.

## Why this exists

AI coding agents are very good at shipping features and very bad at security defaults. Repeated patterns we see in vibe-coded apps:

- Admin API routes with no auth check ("the AI wrote the route, it works, ship it")
- Supabase tables with RLS disabled or `USING (true)`
- `service_role` key in client-bundled code
- `user_metadata.role === 'admin'` checks (user-editable, trivial privilege escalation)
- `.env` committed to the repo
- Debug routes (`/api/test`, `/api/seed`) left in production

This skill encodes the checklist so you don't have to remember it.

## Install

### As a Claude Code skill (personal)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/<you>/vibe-code-security ~/.claude/skills/vibe-code-security
```

Restart Claude Code. The skill is now available and will auto-trigger when you ask for a pre-deploy review.

### As a plugin (shareable)

Coming soon - will publish to a plugin marketplace.

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

Want to add one? See [CONTRIBUTING.md](./CONTRIBUTING.md). Adding a stack is one markdown file - no code.

## How it works

1. Skill reads `package.json` (and other manifests) to detect your stack
2. Loads the relevant checklist(s) from `checks/`
3. Runs grep / file-pattern checks - no LLM hallucinations, every finding points to a real file
4. Reports findings grouped by severity (CRITICAL / HIGH / MEDIUM / LOW)
5. Offers to fix them with your confirmation

## What this is NOT

- Not a replacement for a real pentest
- Not a SAST tool with taint analysis
- Not exhaustive - it catches *common footguns*, not every CVE

The goal: **you won't ship the obvious mistakes**. That's worth a lot when the alternative is "found out at 2am that anon can delete any user."

## License

MIT. Take it, fork it, improve it.

## Credits

Built by [@toanbku](https://github.com/toanbku) for the vibe-coding community.
