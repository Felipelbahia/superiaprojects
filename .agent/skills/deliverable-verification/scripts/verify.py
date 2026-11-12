"""Mechanical checks of a deliverable, driven by the project's JSON config (deliverable-verification).

Usage: python3 -I verify.py --config verification.json
Prints a table `| # | Check | Result | Evidence |` (quote it in the QA file) and exits 1 if any check fails.
A config key that is absent means that check does not run.
"""

import argparse
import csv
import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
from common import csv_shape_errors, files, generated_output, load_config, load_registries, read, split_id  # noqa: E402

DEFAULT_FORBIDDEN = {
    "CPF": r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
    "phone": r"\(?\b\d{2}\)?\s?9?\d{4}-\d{4}\b",
    "e-mail": r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}\b",
    "secret": r"(?i)\b(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",
}


def short(items, limit=12):
    items = sorted(set(items))
    return ", ".join(items[:limit]) + (f" (+{len(items) - limit})" if len(items) > limit else "")


def check_registries(cfg, regs):
    dupes = {name: [i for i, n in Counter(ids).items() if n > 1] for name, ids in regs.items()}
    bad = [f"{name}: duplicated {short(d)}" for name, d in dupes.items() if d]
    for name, spec in cfg["registries"].items():
        bad += [f"{name}: {err}" for err in csv_shape_errors(cfg["_root"], spec)]
    sizes = ", ".join(f"{name} {len(ids)} rows" for name, ids in regs.items())
    return not bad, "; ".join(bad) or sizes


def check_counts(cfg, regs):
    bad, seen = [], 0
    for rule in cfg["counts"]:
        labels = {k.lower(): v for k, v in rule["labels"].items()}
        pattern = re.compile(rule["regex"], re.I)
        for rel in files(cfg["_root"], rule["files"]):
            for number, label in pattern.findall(read(cfg["_root"], rel)):
                seen += 1
                expected = len(regs[labels[label.lower()]])
                if int(number) != expected:
                    bad.append(f"{rel}: '{number} {label}' (registry {labels[label.lower()]}: {expected})")
    return not bad, "; ".join(bad) or f"{seen} counts match the registries"


def check_references(cfg, regs):
    bad, seen = [], 0
    for rule in cfg["references"]:
        known = set(regs[rule["registry"]])
        exclude = list(rule.get("exclude", [])) + generated_output(cfg)
        for rel in files(cfg["_root"], rule["files"], exclude):
            for ref in set(re.findall(rule["regex"], read(cfg["_root"], rel))):
                seen += 1
                if ref not in known:
                    bad.append(f"{rel}: {ref}")
    return not bad, ("unknown ids: " + short(bad)) if bad else f"{seen} references resolve"


def check_index(cfg, regs):
    spec, root = cfg["index"], cfg["_root"]
    cited = re.findall(spec.get("regex", r"`([\w\-./ ]+\.\w+)`"), read(root, spec["file"]))
    places = spec.get("search", ["."])
    missing = [name for name in cited if not any((root / place / name).exists() for place in places)]
    unlisted = [rel for rel in files(root, spec.get("must_list", [])) if rel not in cited]
    problems = (["cited but missing: " + short(missing)] if missing else []) + \
               (["not in the index: " + short(unlisted)] if unlisted else [])
    return not problems, "; ".join(problems) or f"{len(cited)} cited files exist; every must_list file is cited"


def check_generated(cfg, regs):
    return build.is_current(cfg)


def check_source_coverage(cfg, regs):
    missing, total = [], 0
    for rule in cfg["source_coverage"]:
        cited = files(cfg["_root"], rule["cited_in"], generated_output(cfg))
        text = "\n".join(read(cfg["_root"], rel) for rel in cited)
        for rel in files(cfg["_root"], [rule["sources"]]):
            total += 1
            token = Path(rel).stem if rule.get("match") == "stem" else Path(rel).name
            if token not in text:
                missing.append(rel)
    return not missing, f"{total - len(missing)}/{total} sources cited" + (f"; not cited: {short(missing)}" if missing else "")


def check_forbidden(cfg, regs):
    spec = cfg["forbidden"]
    patterns = dict(DEFAULT_FORBIDDEN) if spec.get("defaults", True) else {}
    patterns.update(spec.get("patterns", {}))
    allow = [re.compile(a) for a in spec.get("allow", [])]
    hits = []
    exclude = list(spec.get("exclude", [])) + generated_output(cfg)
    # CSV tables copied into the generated document are scanned too: it is excluded above
    tables = [s["csv"] for s in cfg.get("document", {}).get("sections", []) if isinstance(s, dict)]
    scanned = files(cfg["_root"], spec["files"], exclude)
    for rel in scanned + [t for t in tables if t not in scanned and (cfg["_root"] / t).exists()]:
        text = read(cfg["_root"], rel)
        for label, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                if not any(a.search(match.group(0)) for a in allow):
                    hits.append(f"{rel}: {label}")
    return not hits, ("found " + short(hits)) if hits else f"{len(patterns)} patterns, no match"


def check_required_mentions(cfg, regs):
    missing, total = [], 0
    for rule in cfg["required_mentions"]:
        terms = list(rule.get("terms", []))
        if "registry" in rule:
            since = split_id(rule["since"])
            terms += [i for i in regs[rule["registry"]]
                      if split_id(i) and split_id(i)[0] == since[0] and split_id(i)[1] >= since[1]]
        where = files(cfg["_root"], rule["files"], generated_output(cfg))
        text = "\n".join(read(cfg["_root"], rel) for rel in where)
        total += len(terms)
        missing += [t for t in terms if t not in text]
    return not missing, f"{total - len(missing)}/{total} mentioned" + (f"; missing {short(missing)}" if missing else "")


def check_loop_counter(cfg, regs):
    folder = cfg["_root"] / cfg["loop_counter"]["folder"]
    numbers = [int(m.group(1)) for m in (re.match(r"(\d{2}) ", p.name) for p in folder.glob("*.md")) if m]
    if not numbers:
        return False, f"no 'NN Name.md' files in {cfg['loop_counter']['folder']}"
    dupes = [n for n, c in Counter(numbers).items() if c > 1]
    expected = list(range(0, max(numbers) + 1))
    gaps = sorted(set(expected) - set(numbers))
    ok = not dupes and not gaps
    return ok, f"00-{max(numbers):02d} in sequence" if ok else f"gaps {gaps}; repeated {sorted(dupes)}"


def check_unique_columns(cfg, regs):
    bad = []
    for rule in cfg["unique_columns"]:
        with open(cfg["_root"] / rule["file"], newline="", encoding="utf-8-sig") as handle:
            values = [row[rule["column"]] for row in csv.DictReader(handle, delimiter=rule.get("delimiter", ","))]
        dupes = [v for v, n in Counter(values).items() if n > 1]
        if dupes:
            bad.append(f"{rule['file']}.{rule['column']}: {short(dupes)}")
    return not bad, "; ".join(bad) or "no repeated values"


CHECKS = [
    ("registries", check_registries),
    ("counts", check_counts),
    ("references", check_references),
    ("index", check_index),
    ("document", check_generated),
    ("source_coverage", check_source_coverage),
    ("forbidden", check_forbidden),
    ("required_mentions", check_required_mentions),
    ("loop_counter", check_loop_counter),
    ("unique_columns", check_unique_columns),
]


def custom_checks(cfg):
    """Project-specific checks: every `check_*(ctx)` function in the module named by `custom_checks`."""
    path = cfg["_config_dir"] / cfg["custom_checks"]
    spec = importlib.util.spec_from_file_location("verification_custom", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return [(name[len("check_"):], getattr(module, name)) for name in sorted(dir(module)) if name.startswith("check_")]


def run(cfg):
    """Return [(check, ok, evidence)] for every configured check; a crash counts as a failure."""
    results = []
    try:
        regs = load_registries(cfg) if "registries" in cfg else {}
    except Exception as error:  # e.g. a registry file that does not exist: report it, run the rest
        dependent = [k for k in ("counts", "references", "required_mentions") if k in cfg]
        regs, cfg = {}, {k: v for k, v in cfg.items() if k not in ("registries", *dependent)}
        results.append(("registries", False, f"could not load registries: {type(error).__name__}: {error}"
                        + (f" (not run: {', '.join(dependent)})" if dependent else "")))
    try:
        custom = custom_checks(cfg) if "custom_checks" in cfg else []
    except (Exception, SystemExit) as error:  # a broken custom module must fail loudly, never stop the table
        custom = []
        results.append(("custom:load", False, f"could not load {cfg['custom_checks']}: {type(error).__name__}: {error}"))
    selected = [(key, fn) for key, fn in CHECKS if key in cfg]
    ctx = {"root": cfg["_root"], "config": cfg, "registries": regs}
    for key, fn in selected + [(f"custom:{n}", f) for n, f in custom]:
        try:
            ok, note = fn(ctx) if key.startswith("custom:") else fn(cfg, regs)
        except (Exception, SystemExit) as error:  # a broken check must fail loudly, never pass
            ok, note = False, f"check crashed: {type(error).__name__}: {error}"
        results.append((key, ok, str(note).replace("|", "/")))
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    results = run(load_config(parser.parse_args().config))
    print("| # | Check | Result | Evidence |\n|---|---|---|---|")
    for number, (key, ok, note) in enumerate(results, 1):
        print(f"| {number} | {key} | {'OK' if ok else 'FAIL'} | {note} |")
    failed = sum(not ok for _, ok, _ in results)
    print(f"\n{len(results) - failed}/{len(results)} checks OK")
    return 1 if failed or not results else 0


if __name__ == "__main__":
    sys.exit(main())
