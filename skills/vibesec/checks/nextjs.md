# Next.js checks

Run every check below. For each, report findings under the right severity. Cite file + line.

---

## CRITICAL

### N-C1. API/route handlers without auth
**Look for:** Files matching `app/api/**/route.{ts,js}` or `pages/api/**/*.{ts,js}` that handle non-GET methods (POST/PUT/DELETE/PATCH) and contain admin-ish names (`admin`, `delete`, `users`, `payments`, `webhook`, `internal`).
**Verify:** Open the file. Does it check auth before doing work? Common auth patterns to recognize:
- `await auth()` / `getServerSession()` / `await createClient().auth.getUser()`
- Middleware-applied auth (check `middleware.ts` to confirm the path is matched)
- API key / bearer token check at the top of the handler

**Flag if:** Handler mutates data with no auth check visible in the file or middleware.
**Why this is bad:** Anyone on the internet can call the endpoint. The classic "I vibe-coded an admin panel and someone deleted my data" story starts here.
**Fix template:**
```ts
const { data: { user } } = await supabase.auth.getUser()
if (!user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
// + role check if this is an admin endpoint
```

### N-C2. `NEXT_PUBLIC_` prefix on a secret
**Look for:** `grep -rn "NEXT_PUBLIC_" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.env*"` then filter for names that suggest secrets: `*_SECRET`, `*_KEY`, `*_TOKEN`, `SERVICE_ROLE`, `STRIPE_SECRET`, `*_PRIVATE`.
**Why this is bad:** Anything `NEXT_PUBLIC_*` is inlined into the client bundle. The "secret" is on every visitor's machine.
**Fix:** Drop the `NEXT_PUBLIC_` prefix and only read the var from server code (Route Handlers, Server Components, Server Actions, `middleware.ts`).

### N-C3. Service-role / admin client imported from client component
**Look for:** Files that import a Supabase admin / service-role client AND contain `"use client"` at the top, OR are imported (transitively) by a `"use client"` file.
**Why this is bad:** The admin key ends up in the client bundle. Game over - attacker has full DB.
**Fix:** Move admin-key code to a Route Handler or Server Action. The client should call that route, never hold the key.

---

## HIGH

### N-H1. Server Action without auth check
**Look for:** Files containing `"use server"` (top of file) or inline `async function ... { "use server" ... }`. For each exported async function, check whether it validates auth/ownership before doing work.
**Why this is bad:** Server Actions are callable from any client - the form binding is a convenience, not a security boundary. An attacker can call `myAction({...})` from DevTools.
**Fix:** Re-check auth + ownership inside every Server Action. Don't trust hidden form fields.

### N-H2. Middleware not protecting the routes you think it does
**Look for:** `middleware.ts` (or `middleware.js`) at project root. Read its `config.matcher`. Compare against `app/api/**` and `app/(admin)/**` routes.
**Flag if:** Admin/API routes exist that are not covered by the matcher AND don't have inline auth.
**Why this is bad:** A regex typo in matcher leaves whole route trees unprotected.

### N-H3. Debug / test routes left in
**Look for:** Route files named `debug`, `test`, `dev`, `seed`, `_dev`, `__test`, or commented-out auth checks (`// TODO: add auth`, `// FIXME: auth`).
**Why this is bad:** Forgotten debug endpoints are a top source of breaches.
**Fix:** Delete them, or gate behind `process.env.NODE_ENV !== 'production'` AND a strong token.

### N-H4. CORS wide-open on non-public endpoints
**Look for:** `Access-Control-Allow-Origin: *` set on routes that accept credentials or do mutations. Grep `Access-Control-Allow-Origin` and `cors(` (popular package).
**Why this is bad:** Any site can call your API on behalf of a logged-in user.

---

## MEDIUM

### N-M1. Missing security headers
**Look for:** `next.config.{js,mjs,ts}` - check for a `headers()` function setting CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy, Strict-Transport-Security.
**Why this is bad:** Defense-in-depth. CSP in particular blocks a huge class of XSS.

### N-M2. Source maps shipped to production
**Look for:** `next.config.*` setting `productionBrowserSourceMaps: true`, or `.map` files in `public/`.
**Why this is bad:** Hands attackers your source. Not a vuln by itself but multiplies the impact of every other issue.

### N-M3. Error pages leak stack traces
**Look for:** Custom `error.tsx` / `global-error.tsx` that render `error.message` or `error.stack` directly.
**Why this is bad:** Stack traces reveal file paths, dependency versions, and sometimes secrets.

### N-M4. Hardcoded `dangerouslySetInnerHTML` from user input
**Look for:** `dangerouslySetInnerHTML` usage. For each, trace the source - is the HTML user-controlled?
**Why this is bad:** Direct XSS if user-controlled.

---

## LOW

### N-L1. `revalidate: 0` everywhere (perf, but worth flagging)
### N-L2. `robots.txt` missing for staging
### N-L3. `next dev` running in prod (check start script in `package.json`)
