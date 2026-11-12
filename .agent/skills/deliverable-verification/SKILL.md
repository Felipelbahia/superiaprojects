---
# Repository: https://github.com/Felipelbahia/superiaprojects
name: deliverable-verification
description: Use when a document, report or diagnosis is graded in an execution-loop QA, when a deliverable is assembled from several parts or registries (findings, questions, backlog), when adding a part, finding or id to such a deliverable, or when a file says it is generated and must not be edited by hand.
author: Futuro Mercado / Felipe Bahia (@felipelbahia)
license: MIT
---
# Deliverable Verification

## Overview

Large deliverables break silently: a count goes stale, a part never reaches the index, an id is cited that does not exist, the generated file is edited by hand, a CPF leaks. Re-reading catches some of it and costs tokens every cycle. This skill gives every project the same three generic scripts, driven by one JSON config per project:

| Script | Does | Exit code |
|---|---|---|
| `scripts/verify.py --config C` | Mechanical checks, printed as a table `\| # \| Check \| Result \| Evidence \|` | 1 if any check fails |
| `scripts/build.py --config C [--check]` | Assembles the single document from its parts (optional piece) | `--check`: 1 if the file on disk is stale |
| `scripts/next_id.py --config C` | Next free id of each registry, per prefix | 0 |

Run them from the kit: `python3 -I "/Users/macbookpro/Documents/IA Projects/_Plataforma/0 Padrões/.agent/skills/deliverable-verification/scripts/verify.py" --config verification.json`. A project that must be self-contained copies `scripts/` **unchanged** into its repo; only the config is project-specific. Standard library only.

Generalized from a real diagnosis (13 parts, 340 KB) whose verification script failed real items in two review cycles before any human reviewer.

## When to Use

- **QA of an execution-loop** with document-shaped items: `verify.py` is the "verification script kept in the repository" that the loop's *Who grades* rule requires for mechanical items. Quote its table as evidence.
- **A deliverable built from parts** (`parts/*.md` + registries + one generated file): use `build.py` too.
- **Adding a part, finding, question or backlog row**: use `next_id.py`, never guess an id.
- **Not for** fidelity ("does the text match the screen/source?"): that is the independent reviewer's job in the execution-loop. Not for code with its own test suite.

## Rules

1. **The generated file is never edited by hand.** Edit the part or the registry, run `build.py`, then `verify.py`. A file whose first lines say "generated" is rebuilt, even under deadline.
2. **Ids come from `next_id.py`.** Looking at the last row misses ids elsewhere in the file and reused ids.
3. **Counts are rows, not ids.** A backlog row `2b` is a row; `verify.py` counts it.
4. **Run the whole `verify.py` every cycle and after every change.** It costs no tokens; partial runs miss the regressions it exists to catch.
5. **Every error a reviewer finds that a pattern could catch becomes a check** (a config entry or a `check_*` in the custom file), so it never needs a reviewer again.
6. **Deliver only with `N/N checks OK`.** A failing check is fixed in the parts, not silenced in the config; changing the config to make it pass needs the owner's OK.

## Adopting it in a project (3 steps)

1. Copy `verification.example.json` next to the deliverable as `verification.json`; set `root`, delete the keys you do not need, fill the rest (every key is explained in its `_key` field).
2. If `document` is used: run `build.py` once and add the "generated, do not edit" line to the index.
3. Run `verify.py`; fix the parts until all checks pass. Project-only rules go to `verification_custom.py` as `def check_<name>(ctx): return ok, evidence` (`ctx`: `root`, `config`, `registries`).

## Config keys (each key present = that check runs)

| Key | Fails when |
|---|---|
| `registries` | an id repeats in a registry (also defines the registries the other checks use) |
| `counts` | a number written next to a label differs from the registry row count |
| `references` | a cited id does not exist in its registry |
| `index` | the index cites a file that does not exist, or a `must_list` file (e.g. `parts/*.md`) is not cited |
| `document` | the generated file differs from a fresh build (dates ignored) or a configured part is missing |
| `source_coverage` | a source file (screenshot, export) is not cited by name in any part |
| `forbidden` | CPF, phone, e-mail, secret (defaults) or a project pattern appears in `files` or in a CSV table of `document.sections`, unless an `allow` regex matches |
| `required_mentions` | a term, or a registry id from `since` on, is missing from the given files |
| `loop_counter` | the loop folder's `NN Name.md` numbers have a gap or a repeat |
| `unique_columns` | a CSV column repeats a value |
| `custom_checks` | a project `check_*` returns False or crashes |

## Tests

`python3 -B -I -m unittest discover -s "<this skill>/tests" -v` — a correct example project (`tests/fixture/`) must pass every check, and each check has a test that plants its error and requires FAIL. Change a script → run the suite.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Rewriting the generated file by hand "because there is no time" | Edit the part, `build.py`, `verify.py`: three commands, faster than a manual merge |
| Picking the next id by eye | `next_id.py` |
| Writing a project-specific copy of `verify.py` | Config + `verification_custom.py`; scripts stay identical everywhere |
| Loosening a regex or deleting a key to turn a FAIL green | Fix the deliverable; config changes that relax a check need the owner |
| Treating `N/N OK` as proof that the text matches its sources | It proves mechanics only; fidelity needs the independent reviewer |
