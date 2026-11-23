-- Supabase / Postgres access audit. READ-ONLY: only SELECTs.
-- Run in the SQL editor, `psql`, or the Supabase MCP `execute_sql`. Review every row returned.
-- Not executed against a database by the author of this file: syntax-checked only.

-- 01 CRITICAL: tables in the exposed schema WITHOUT row level security
select n.nspname as schema, c.relname as "table"
from pg_class c join pg_namespace n on n.oid = c.relnamespace
where c.relkind in ('r', 'p') and n.nspname = 'public' and not c.relrowsecurity
order by 2;

-- 02 INFO: RLS on but no policy (table is locked for API roles; confirm that is intended)
select n.nspname as schema, c.relname as "table"
from pg_class c join pg_namespace n on n.oid = c.relnamespace
where c.relkind in ('r', 'p') and n.nspname = 'public' and c.relrowsecurity
  and not exists (select 1 from pg_policies p where p.schemaname = n.nspname and p.tablename = c.relname)
order by 2;

-- 03 REVIEW: every policy in public and storage, to read by hand
select schemaname, tablename, policyname, permissive, cmd, roles, qual, with_check
from pg_policies
where schemaname in ('public', 'storage')
order by schemaname, tablename, policyname;

-- 04 HIGH: policies that never mention auth.uid() / auth.jwt() (look for `true` or client-supplied values)
select schemaname, tablename, policyname, cmd, roles, qual, with_check
from pg_policies
where schemaname = 'public'
  and coalesce(qual, '') !~* 'auth\.(uid|jwt)\(' and coalesce(with_check, '') !~* 'auth\.(uid|jwt)\(';

-- 05 HIGH: UPDATE / ALL policies with no WITH CHECK (a user may rewrite columns such as role or user_id)
select schemaname, tablename, policyname, cmd, qual
from pg_policies
where schemaname in ('public', 'storage') and cmd in ('UPDATE', 'ALL') and with_check is null;

-- 06 HIGH: policies built on user_metadata (the signed-in user can edit it)
select schemaname, tablename, policyname, cmd, qual, with_check
from pg_policies
where coalesce(qual, '') ~* 'user_metadata' or coalesce(with_check, '') ~* 'user_metadata';

-- 07 HIGH: write policies open to anon / public
select schemaname, tablename, policyname, cmd, roles
from pg_policies
where cmd <> 'SELECT' and ('anon' = any(roles) or 'public' = any(roles));

-- 08 HIGH: views in public that bypass RLS (no security_invoker)
select n.nspname as schema, c.relname as view_name, c.reloptions
from pg_class c join pg_namespace n on n.oid = c.relnamespace
where c.relkind = 'v' and n.nspname = 'public'
  and not (coalesce(c.reloptions, '{}'::text[]) && array['security_invoker=on', 'security_invoker=true']);

-- 09 HIGH: SECURITY DEFINER functions in the exposed schema (and whether search_path is pinned)
select n.nspname as schema, p.proname as function_name,
       pg_get_function_identity_arguments(p.oid) as args,
       p.proconfig as config,
       (p.proconfig is not null and exists (select 1 from unnest(p.proconfig) s where s like 'search_path=%')) as search_path_pinned
from pg_proc p join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public' and p.prosecdef;

-- 10 HIGH: functions in public that anon can execute
select n.nspname as schema, p.proname as function_name, pg_get_function_identity_arguments(p.oid) as args
from pg_proc p join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public' and p.prokind = 'f' and has_function_privilege('anon', p.oid, 'execute');

-- 11 HIGH: tables where anon holds write privileges
select table_schema, table_name, privilege_type
from information_schema.role_table_grants
where grantee = 'anon' and table_schema = 'public' and privilege_type in ('INSERT', 'UPDATE', 'DELETE', 'TRUNCATE');

-- 12 CRITICAL if sensitive files live there: public storage buckets (anyone with the URL reads the files)
select id, name, public, file_size_limit, allowed_mime_types
from storage.buckets
where public;

-- 13 MEDIUM: buckets without size or type limits
select id, name, public, file_size_limit, allowed_mime_types
from storage.buckets
where file_size_limit is null or allowed_mime_types is null;

-- 14 MEDIUM: policies on storage.objects that do not restrict the bucket or the owner folder
select policyname, cmd, roles, qual, with_check
from pg_policies
where schemaname = 'storage' and tablename = 'objects'
  and coalesce(qual, '') !~* 'bucket_id' and coalesce(with_check, '') !~* 'bucket_id';
