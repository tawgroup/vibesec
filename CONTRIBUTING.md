# Contributing

The goal: anyone should be able to add a new stack with **one markdown file** and a one-line edit to `SKILL.md`. No code changes, no build step.

## Adding a new stack

### 1. Copy the template

```bash
cp checks/_template.md checks/<your-stack>.md
```

Naming: lowercase, hyphenated. Examples: `prisma.md`, `drizzle.md`, `sveltekit.md`, `fastapi.md`, `clerk.md`.

### 2. Fill it in

Read `checks/nextjs.md` and `checks/supabase.md` to get a feel for the format. Each check needs:

- **A unique ID** — `<stack-prefix>-<severity>-<num>`. Pick a 1-2 letter stack prefix (P for Prisma, D for Drizzle, etc.).
- **A concrete `Look for` pattern** — exact grep, glob, or file pattern. No "review the code carefully" hand-waves. If a check can't be expressed as a pattern, it doesn't belong here.
- **Why this is bad** — one line describing what the attacker actually does. Make it concrete: "anon can read every row" not "may lead to data exposure."
- **A copy-pasteable fix** — for CRITICAL and HIGH. For MEDIUM/LOW, a short pointer is fine.

### 3. Register the stack in SKILL.md

Add a row to the detection table in `SKILL.md`:

```markdown
| `<package-name>` in dependencies | `checks/<your-stack>.md` |
```

If detection is more nuanced than a single package, describe it in prose under the table.

### 4. Update the README

Move your stack from the 🟡 "wanted" list to the ✅ "supported" list.

### 5. Test it

Run the skill against a real (or contrived) repo using your stack. Confirm:
- Each CRITICAL/HIGH check fires on a deliberately broken example
- Each check produces zero false positives on a clean example
- The report renders cleanly

### 6. Open a PR

Title: `Add <stack> checks`. In the description, link to one real example of each CRITICAL/HIGH issue in the wild if you can find it - it makes the checklist much more convincing.

## Style guide for checks

**Severity discipline.** The whole skill becomes noise if everything is HIGH. Apply these rules:

- **CRITICAL** = unauthenticated remote exploitation, full data exposure, or auth bypass. Attacker needs nothing but a URL.
- **HIGH** = exploitable with minimal effort (logged-in user can escalate, or a known footgun like `USING (true)` RLS).
- **MEDIUM** = defense-in-depth gap or bad practice that's exploitable only in combination with another bug.
- **LOW** = nitpick. Be sparing.

When in doubt, downgrade. It's better to surprise the user with "wow that's worse than I thought" than to numb them with false-criticals.

**No advice without a target.** "Make sure you validate input" is not a check. "Look for `req.body.email` passed directly to `db.query(...)` without zod / Valibot validation" is a check.

**Cite file + line in findings.** The output report must point to a real location. If your check can't, restructure it.

## Things we don't want

- **Generic OWASP top-10 recitations.** This skill exists because OWASP top-10 is not what vibe-coders ship to prod. Stack-specific footguns are.
- **Checks that require running the app.** Static-only. The skill should work on a freshly cloned repo with no install / no DB / no env.
- **Checks that need a live DB.** Read migrations and config files instead.
- **LLM-as-judge checks** ("ask Claude if this is secure"). Use grep patterns - they're deterministic and don't hallucinate.

## Questions?

Open a draft PR or a discussion. Better to ship a rough check that catches a real bug than to perfect it for six months.
