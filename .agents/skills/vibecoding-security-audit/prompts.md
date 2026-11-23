# The 5 audit prompts

Source: the owner's list `Vibecoding - Segurança - Checagem`, section 8 (prompts by @murphmaxxing). Paste one into the coding agent with access to the repository. Run the scripts of the triggered modules first; the prompts then cover what a script cannot read.

## Order

| Prompt | Runs when | Pair with |
|---|---|---|
| 1 Secrets | Always | `vulnerability-scanner` (`security_scan.py`) |
| 2 Authentication and sessions | The product has accounts | `auth-implementation-patterns` |
| 3 Database access (RLS) | Supabase or an exposed database | `supabase-rls.md` + `scripts/rls_audit.sql` |
| 4 Dangerous inputs and uploads | Any user input; uploads | `uploads.md` |
| 5 Money and load | LLM, e-mail, SMS or other usage-priced routes | `ai-routes.md` |

## Report format (all prompts)

One table per run: `where | what is wrong | how an attacker uses it | severity | exact fix`. Severities: CRITICAL, HIGH, MEDIUM. Fix order: public storage and unprotected tables first (silent failures), then secrets, then authorization, then the rest. A key that ever touched a commit is burned: rotate it.

## Prompt 1: secrets

```text
Act as a security researcher auditing my repo for exposed secrets. Find:
1. Hardcoded API keys, tokens, passwords, or connection strings in any file
2. .env files that are committed or missing from .gitignore
3. Secrets in git history even if the file was deleted later
4. Secrets that ship to the browser in frontend code or build output
5. Public/anon keys doing privileged work

Output a table: file and line | what leaked | how an attacker finds it | severity (CRITICAL / HIGH / MEDIUM) | exact fix.
Then list every key I need to rotate. A key that ever touched a commit is burned, hiding it now is not enough.
```

## Prompt 2: authentication and sessions

```text
Attack my authentication like you want in. Walk every auth path in this repo:
1. List every route and API endpoint and whether it verifies a valid session. Flag any that skip it.
2. Session handling: where tokens live, whether they expire, whether logout and password change kill them.
3. Password rules: minimum length, breached-password check, anything my auth provider offers that I left off.
4. Password reset and email verification: can I reset someone else's password, or use the app with an unverified email?

Output: flow | weakness | exact exploit steps | severity | fix.
Any endpoint that trusts a user ID from the request body instead of the session is CRITICAL.
```

## Prompt 3: database access, table by table

```text
Audit my database access rules table by table (Supabase RLS or equivalent):
1. List every table and whether RLS is enabled. Any table reachable with the public key and no RLS is CRITICAL.
2. For each policy, write the exact query user A runs to read or edit user B's rows, and tell me whether it works.
3. Flag policies that filter on values the client sends instead of auth.uid().
4. Check INSERT and UPDATE policies, not just SELECT: can I insert rows pointed at another user, or update columns I shouldn't own, like role or credits?
5. Apply the same checks to storage buckets.

Output: table | policy state | the attack query | what leaks | severity | corrected policy as real SQL.
```

## Prompt 4: dangerous inputs, injection and uploads

```text
Trace every path where user input reaches something dangerous in this repo:
1. SQL or NoSQL queries built with string concatenation or template literals instead of parameters
2. Input passed to eval, exec, child_process, or shell commands
3. File uploads: is the filename sanitized, is the type verified server-side, can I upload an executable or path-traverse with ../
4. User content rendered as HTML without escaping, including dangerouslySetInnerHTML and markdown renderers
5. Endpoints with no server-side validation at all

Output: file and line | input source | what it reaches | a working example payload | severity | fix.
```

## Prompt 5: money and load

```text
Find every endpoint in this app that costs me money or resources when called, and check its protection:
1. Routes that trigger AI or LLM API calls: what stops a script from calling each one 100,000 times tonight? Check auth, per-user limits, per-IP limits.
2. Login, signup, and password reset: rate limits, bot protection, and whether response differences let someone enumerate valid emails.
3. Email or SMS sending routes someone can spam through.
4. Expensive queries or exports with no caps or pagination.
5. Usage metering: is it enforced server-side, and does it fail closed?

Output: endpoint | what one call costs me | the abuse scenario | projected damage from one night | severity | the exact limiter to add.
```

## Third-party skill libraries

A community library of ~800 security skills (`mukul975/Anthropic-Cybersecurity-Skills`) is **not affiliated with Anthropic** and includes offensive, dual-use techniques. If it is installed, read each `SKILL.md` before enabling it, use it only on systems you own or are authorized to test, and run it as a second layer after these prompts. This skill imports nothing from it.
