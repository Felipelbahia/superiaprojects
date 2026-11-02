---
status: draft
approved:
---
# <Module> — SCHEMA fragment (size L)

> Entities of this module only. Builds on the core schema (tenants, users, roles). Every entity carries the tenant column and its rules.

## Entities

### E-<module>-01 <name>
- Purpose · feature (F-<module>-xx):

| Column | Type | Required | Default | Validation | Unique / Index | Reference |
|---|---|---|---|---|---|---|
| tenant | | yes | | | | core tenant |

## Relationships
Inside the module and to other modules. Every reference includes the tenant.

## Access rules

| Entity | Who can create | Read | Update | Delete |
|---|---|---|---|---|

## Isolation checks required by this module
Listed in `ARCHITECTURE.md` section 8; add module-specific ones here (for example exports, public links, PDFs).

## Traceability
| Entity | Supports features |
|---|---|

## Change log

| Date | What changed | Approved by |
|---|---|---|

## Approval record

Date · criteria met · owner decision · reviewer agents
