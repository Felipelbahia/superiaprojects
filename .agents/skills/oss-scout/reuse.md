# Reuse mode

## 1. Classify
One row per capability of the PRD (F-xx). Columns: capability · class · reason (one line).

| Class | Meaning | Examples |
|---|---|---|
| `reuse` | Hard, sensitive or standardized: search for a library or managed service | authentication, payments, PDF, dates and time zones, rich-text editor, drag and drop, encryption, e-mail delivery |
| `platform` | The framework or platform already does it: use that | routing, forms, image optimization, cookies, i18n built into the framework |
| `build` | Trivial (a few lines) or the product's differentiator | character counter, a simple filter, the core business rule |

**Rule of thumb:** reuse the hard, sensitive or standardized; write the trivial; use what the platform ships. In a personal MVP, lean to reuse and managed services, inside the lean budget and the security baseline. `platform` and `build` rows never trigger a search.

Doubt between `reuse` and `build`: if a mistake would cost security, money or data, it is `reuse`. If it is under about 30 lines and low risk, it is `build`.

## 2. Search
Tools, in order: Context7 (`resolve-library-id`, `query-docs`; reputation, snippets, version) → Firecrawl search with `categories: ["developer"]` → the registry (`npm view <pkg> version license dist-tags time.modified peerDependencies deprecated`) → official site. `gh` may be absent: do not depend on it. Candidates: 2-3, each with source and date.

## 3. Criteria (all 8; each with source and date)
1. **Maintenance:** last release, open critical issues, response to issues.
2. **Adoption:** weekly downloads or equivalent, known users.
3. **License:** class from `reference-study.md` policy table.
4. **Weight:** size and transitive dependencies (lean budget).
5. **Security:** known advisories for the version, deprecation flags.
6. **Fit:** compatible with the `## Stack` block and the installed versions. Compare peer and direct dependency ranges with the lockfile; a conflict (for example the candidate needs a newer Zod than installed) goes to the owner as an option, never a silent upgrade.
7. **Docs quality:** setup, examples for the installed version.
8. **Exit cost:** how hard it is to remove or replace later.

Facts you did not look up are written "not verified". Never "popular" or "maintained" from memory.

## 4. Verify the package (anti-slopsquatting)
Before recommending or installing:
1. It exists in the registry (`npm view <exact name>` or the ecosystem's equivalent). 404 = stop.
2. The repository URL declared by the package matches the project you read about.
3. Age, downloads and maintainers are plausible; a very new package with few downloads is a flag.
4. The name is not a variation of a famous one (swapped letters, extra suffix such as `-pro`, `-ultra`).
5. Install scripts (`preinstall`, `postinstall`) are read before installing.

Any failure: do not install; record "not verified" and the reason; offer verified alternatives.

## 5. Register and ask
Fill `templates/CAPABILITIES.md` in ARCHITECTURE (if ARCHITECTURE does not exist yet, keep it as its own file to merge in as a section) and the dependency register. Decisions with cost, a new dependency or lock-in go to the owner as 2-3 options with a recommended default, in the owner's language. Never install before the owner approves the dependency.
