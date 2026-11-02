# Ops Resilience (paid APIs, backend, mobile OTA)

Apply when the project calls paid APIs or runs a remote backend. Each item: what, then how to verify.

| Item | Do | Verify |
|---|---|---|
| Hard spend cap | Set a **hard** monthly limit (not just an alert) in every paid provider (LLM, SMS, email, cloud). Add a usage alert at 50% and 80%. | Open each provider's billing page; screenshot or note the limit value |
| LLM credit balance | Alert on fast burn, not only on low balance | Alert exists and fires on a test threshold |
| Free plan that pauses | Supabase pauses Free projects with low activity over 7 days (verificado 2026-10-12, supabase.com/docs/guides/platform/free-project-pausing). Move production to a paid plan | Project plan shown in dashboard |
| Restore rehearsal | Restore the latest backup into a scratch project and read real rows | Written date of the last successful restore; a never-restored backup is not a backup |
| Kill switch | Remote flag read by the backend/app to disable one feature or the whole app without deploying | Flip the flag in staging, observe the feature off within one minute |
| Mobile hotfix | Expo apps: EAS Update ships JS changes without store review; `eas update --rollout-percentage=10` rolls out gradually and a rollout can be reverted (verificado 2026-10-12, docs.expo.dev/eas-update/rollouts). Native changes still need a new build and a new runtimeVersion | One test update reaches a real device |

## Kill switch pattern (one table, one check)

```sql
-- feature_flags: key text primary key, enabled boolean not null default true, message text
create table feature_flags (key text primary key, enabled boolean not null default true, message text);
alter table feature_flags enable row level security;
create policy "read flags" on feature_flags for select using (true);
-- writes only via service role / dashboard
```

```ts
// Gate every costly or risky path (chatbot, signup, payments) on the flag.
export async function featureEnabled(key: string): Promise<boolean> {
  const { data } = await supabase.from('feature_flags').select('enabled').eq('key', key).single();
  return data?.enabled ?? false; // fail closed if the flag cannot be read
}
```

Fail closed for paid or risky features (chatbot), fail open for core read paths. Cache for at most 30-60 s so the switch is fast but cheap.
