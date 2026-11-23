# AI and paid routes: denial-of-wallet and injection

Only when the project calls an LLM, SMS, e-mail or any usage-priced API. Goal: no script can turn one night of requests into a bill, and the model cannot be talked into acting.

## Defense layers (all of them, in this order)

| Layer | Rule | Where |
|---|---|---|
| 1. Provider hard cap | A hard monthly limit in the provider dashboard, plus alerts at 50% and 80% | `launch-readiness/ops-resilience.md` |
| 2. Kill switch | A remote flag the route checks first; fail closed for paid routes | `launch-readiness/ops-resilience.md` |
| 3. Auth first | Identity comes from the verified session, never from the request body | server |
| 4. Per-user quota | Atomic daily budget per user, enforced in the database (below) | server |
| 5. Per-request caps | Max input size, `max_tokens`/output cap, no user-supplied model name | server |
| 6. Per-IP limit and bot check | For signup, login, reset and any unauthenticated route that costs money | edge/WAF |
| 7. Fail closed | If the quota check errors, deny; never "allow on error" | server |

## Atomic per-user quota (Postgres)

```sql
create table public.ai_usage (
  user_id uuid not null references auth.users on delete cascade,
  day date not null default current_date,
  used_cents integer not null default 0,
  primary key (user_id, day)
);
alter table public.ai_usage enable row level security;  -- no policy: only the service role touches it

create or replace function public.consume_ai_quota(p_user uuid, p_cost_cents integer, p_limit_cents integer)
returns boolean
language plpgsql
as $$
declare ok boolean;
begin
  if p_cost_cents > p_limit_cents then return false; end if;
  insert into public.ai_usage as u (user_id, day, used_cents)
  values (p_user, current_date, p_cost_cents)
  on conflict (user_id, day)
  do update set used_cents = u.used_cents + excluded.used_cents
  where u.used_cents + excluded.used_cents <= p_limit_cents
  returning true into ok;
  return coalesce(ok, false);  -- no row returned means over the limit
end $$;
revoke execute on function public.consume_ai_quota from public, anon, authenticated;
grant execute on function public.consume_ai_quota to service_role;
```

## Route guard (Edge Function, TypeScript)

```ts
const DAILY_LIMIT_CENTS = 50
const ESTIMATE_CENTS = 2          // worst-case cost of one call with your max_tokens

export async function guardedCall(admin: SupabaseClient, userId: string, run: () => Promise<Response>) {
  if (!(await featureEnabled(admin, 'ai_chat'))) return json(503, 'temporarily unavailable')   // kill switch
  const { data: ok, error } = await admin.rpc('consume_ai_quota', {
    p_user: userId, p_cost_cents: ESTIMATE_CENTS, p_limit_cents: DAILY_LIMIT_CENTS,
  })
  if (error || ok !== true) return json(429, 'daily limit reached')   // fail closed on error
  return run()   // provider call with max_tokens set and a fixed model
}
```

`featureEnabled` is the kill switch pattern in `launch-readiness/ops-resilience.md`. Call the guard before the provider; reconcile the real cost afterwards if you need exact accounting.

## Prompt injection (text from third parties reaches the model)

- Keep instructions and untrusted data apart; wrap the data in delimiters (for example `<user_input>...</user_input>`) and say it is data.
- Treat the model's output as untrusted: validate it, never run it as code or SQL, never render it as raw HTML.
- Give the model no tool that deletes, pays, sends or publishes without a human confirmation step.
- The model never has access to other users' data: it receives only what the signed-in user may read.

## Audit

Run prompt 5 in `prompts.md`; every endpoint that costs money must name its limiter. Test the quota by hand: call until the limit, expect `429`, then raise the cost above the limit, expect `429`.
