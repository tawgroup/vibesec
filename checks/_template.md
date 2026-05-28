# <Stack Name> checks

> **For contributors:** Copy this file to `checks/<your-stack>.md` and fill it in. Then add a detection rule in `SKILL.md` so the skill knows when to load your file.
>
> **Naming:** lowercase, hyphenated. Examples: `prisma.md`, `drizzle.md`, `sveltekit.md`, `fastapi.md`, `clerk.md`, `firebase.md`.
>
> **Tone:** terse, specific, actionable. Every check must have a real grep/file-pattern to look for, a clear "why it's bad" reason, and a copy-pasteable fix. No vague advice.
>
> **ID prefix:** Use the first letter(s) of your stack. e.g., Prisma = `P-`, Drizzle = `D-`, Clerk = `CK-`. Then C/H/M/L for severity, then a number. Example: `P-C1` = Prisma Critical #1.

Run every check below. For each, report findings under the right severity. Cite file + line.

---

## CRITICAL

### <ID>. <Short title>
**Look for:** <exact grep / glob / file pattern>
**Why this is bad:** <one-line attack scenario - what does the attacker actually do?>
**Fix template:**
```<lang>
// code that fixes it, copy-pasteable
```

---

## HIGH

### <ID>. <Short title>
**Look for:**
**Why this is bad:**
**Fix:**

---

## MEDIUM

### <ID>. <Short title>
**Look for:**
**Why this is bad:**

---

## LOW

### <ID>. <Short title>

---

## Checklist before opening the PR

- [ ] Every check has a concrete `Look for` pattern (no "review the code carefully" hand-waves)
- [ ] Every CRITICAL/HIGH check has a copy-pasteable fix
- [ ] You added the detection rule to `SKILL.md` under "Detect the stack"
- [ ] You updated `README.md`'s supported-stacks list
- [ ] You tested the checklist against at least one real (or contrived) repo
