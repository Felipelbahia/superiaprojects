# Supabase RLS audit

Only when the project uses Supabase (or Postgres exposed through an API). The mechanical part is `scripts/rls_audit.sql` (14 read-only queries); the judgment part is reading each policy as an attacker.

Facts below were checked against the Supabase docs on 2026-10-12 (supabase.com/docs/guides/database/postgres/row-level-security, /guides/storage/security/access-control, /guides/storage/buckets/fundamentals, /guides/database/functions, lint 0010). Re-check them when the date is old.

## Rules the audit enforces

| Rule | Why | Query |
|---|---|---|
| RLS enabled on every table in an exposed schema (`public` by default). Tables created in raw SQL do not get it automatically | Without it the public key reads and writes the whole table | 01, 02 |
| Policies filter on `auth.uid()` (written `(select auth.uid())`), never on values the client sends | Client-supplied ids let user A act as user B | 04 |
| Unauthenticated `auth.uid()` is `null`; add `auth.uid() is not null` when the intent matters, and set `TO authenticated` | A silent `null = user_id` hides the intent and runs for `anon` | 03, 04 |
| `UPDATE` needs `USING` **and** `WITH CHECK`; an `UPDATE` also needs a `SELECT` policy | Without `WITH CHECK` a user can rewrite `user_id` or `role` | 05 |
| Never authorize from `user_metadata`; use `app_metadata` | The signed-in user can edit `user_metadata` | 06 |
| `anon` has no write policy or write grant unless the route is truly public | Anyone on the internet can write | 07, 11 |
| Views in `public` use `with (security_invoker = true)` (Postgres 15+) | Views run as their creator and bypass RLS by default (advisor lint 0010) | 08 |
| `security definer` functions pin `search_path` and do not live in an exposed schema; revoke `execute` from `public`/`anon` unless intended | They run with the creator's privileges and are callable by any role by default | 09, 10 |
| Buckets private by default; a public bucket skips access control for reads | Public means anyone with the URL reads the file | 12 |
| Buckets set size and allowed types; `storage.objects` policies name the bucket and the owner folder | Uploads need an `INSERT` policy; limits belong at the bucket | 13, 14 |
| The secret key (`service_role` / `sb_secret_...`) never ships to a client | It bypasses RLS entirely | prompts 1 and 3 |

## Procedure

1. Run the queries with the Supabase MCP (`execute_sql`; also `get_advisors` for security and performance lints) or `psql`. Do not change anything while auditing.
2. For every policy in query 03 write the attack: the exact statement user A runs against user B's row. If it succeeds, it is a finding.
3. Report: table | policy state | attack query | what leaks | severity | corrected SQL. Apply fixes as a migration, never by hand in production.
4. Re-run the queries after the fix; the list must shrink.

## Reference fixes

```sql
alter table public.notes enable row level security;
create policy "own notes" on public.notes
  for update to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
create view public.order_totals with (security_invoker = true) as
  select user_id, sum(total_cents) as total from public.orders group by user_id;
```

Optional guardrail: an event trigger that enables RLS on each new table is in the Supabase RLS docs ("Auto-enable RLS for new tables"); it only affects tables created after it is installed.
