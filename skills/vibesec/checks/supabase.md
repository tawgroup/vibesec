# Supabase checks

Run every check below. For each, report findings under the right severity. Cite file + line.

For DB checks (RLS, policies), prefer reading migration files in `supabase/migrations/` over running live SQL. If the user has the Supabase MCP installed and explicitly asks to query live, you can - but never auto-connect to a production DB.

---

## CRITICAL

### S-C1. RLS disabled on a user-data table
**Look for:** In `supabase/migrations/*.sql`, every `CREATE TABLE` statement. For each, check whether a matching `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` exists.
**Special attention:** tables named `users`, `profiles`, `orders`, `messages`, `posts`, `subscriptions`, `payments`, anything user-owned.
**Why this is bad:** Without RLS, the anon key can read/write every row. This is the #1 vibe-code Supabase footgun.
**Fix template:**
```sql
ALTER TABLE public.<table> ENABLE ROW LEVEL SECURITY;
CREATE POLICY "users read own" ON public.<table>
  FOR SELECT USING (auth.uid() = user_id);
```

### S-C2. `service_role` / secret key in client-side code
**Look for:** `grep -rn "service_role\|SUPABASE_SERVICE_ROLE\|sb_secret_" --include="*.ts" --include="*.tsx" --include="*.js"`. Any match in a file that is client-bundled (anything under `"use client"` or imported by one) is critical. Also flag `NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY` (or any `NEXT_PUBLIC_*` var holding an `sb_secret_` key) immediately.
**Note on key formats:** Supabase's new API keys look like `sb_secret_...` (secret, server-only) and `sb_publishable_...` (safe for the browser, replaces the anon key). An `sb_secret_` key has the same power as the legacy `service_role` JWT — same rule applies.
**Why this is bad:** service_role / `sb_secret_` bypasses RLS. Leaking it = full DB access for anyone.
**Fix:** Only use the secret key in Route Handlers / Server Actions / Edge Functions. Read from `process.env.SUPABASE_SERVICE_ROLE_KEY` or `process.env.SUPABASE_SECRET_KEY` (no `NEXT_PUBLIC_`).

### S-C3. Authorization driven by `user_metadata`
**Look for:** `grep -rn "user_metadata" --include="*.ts" --include="*.tsx" --include="*.sql"`. Flag any usage in:
- RLS policies (`USING (auth.jwt() ->> 'user_metadata' ...)`)
- Role checks in API code (`if (user.user_metadata.role === 'admin')`)

**Why this is bad:** `user_metadata` is **user-editable from the client**. A user can self-promote to admin via `supabase.auth.updateUser({ data: { role: 'admin' } })`. Privilege escalation.
**Fix:** Move authorization data to `app_metadata` (server-set, user cannot modify). Update policies to read `auth.jwt() ->> 'app_metadata'`.

---

## HIGH

### S-H1. Permissive RLS policy
**Look for:** Policies with `USING (true)` or `WITH CHECK (true)` - especially on `INSERT`/`UPDATE`/`DELETE`. Read each `CREATE POLICY` in `supabase/migrations/`.
**Why this is bad:** "Enable RLS but policy is `true`" is functionally the same as no RLS.
**Fix:** Tie the policy to `auth.uid()` or another column the user can't forge.

### S-H2. UPDATE policy without a matching SELECT policy
**Look for:** For each table with an UPDATE policy, confirm a SELECT policy also exists.
**Why this is bad:** Postgres needs to SELECT the row before applying UPDATE. Without SELECT policy, UPDATE silently fails (looks like data corruption to the user) or, worse, allows updates that shouldn't be visible.

### S-H3. Views without `security_invoker = true`
**Look for:** `CREATE VIEW` / `CREATE OR REPLACE VIEW` in migrations. Check for `WITH (security_invoker = true)`.
**Why this is bad:** Views default to `security_definer`, which **bypasses RLS of the calling user**. Anon can read everything through the view.
**Fix:**
```sql
CREATE VIEW public.my_view WITH (security_invoker = true) AS ...;
```

### S-H4. Public storage bucket with sensitive data
**Look for:** In migrations or Supabase config: `storage.buckets` entries with `public = true`. Cross-reference bucket names (`avatars` may be OK; `invoices`, `documents`, `private` are not).
**Why this is bad:** Public buckets are listable and downloadable by anyone with the URL pattern.

### S-H5. Edge / DB functions without `SECURITY DEFINER` set correctly
**Look for:** `CREATE FUNCTION ... SECURITY DEFINER` - especially without `SET search_path = ''`.
**Why this is bad:** `SECURITY DEFINER` without a locked search_path is a known privilege-escalation pattern (attacker creates a function in their schema that shadows a built-in).
**Fix:** Always add `SET search_path = ''` (or a specific schema) to `SECURITY DEFINER` functions.

---

## MEDIUM

### S-M1. Auth not revoked on user delete
**Look for:** Code that deletes from `auth.users` or `profiles` without calling `supabase.auth.admin.signOut(userId)` or revoking sessions.
**Why this is bad:** A deleted user's JWT remains valid until expiry (up to 1 hour by default).

### S-M2. No rate limiting on auth endpoints
**Look for:** Custom auth wrappers (sign-in, sign-up, password reset, OTP) without rate limiting. Supabase has built-in limits but custom flows often skip them.

### S-M3. Anon key with broad table grants
**Look for:** `GRANT ... TO anon` statements in migrations. The anon role should only have what's needed.

---

## LOW

### S-L1. Missing `created_at` / `updated_at` audit columns on sensitive tables
### S-L2. No soft-delete on user-owned tables (forensics value)
